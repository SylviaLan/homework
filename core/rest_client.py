"""
REST API 客户端封装：GET/POST/PUT/DELETE/PATCH，统一日志与异常处理。
支持基于 biz status 映射的响应校验；支持按 RestApiDef 自动区分 method 的 request/request_json_success。
"""
import allure
import requests

from config.settings import REST_BASE_URL, REST_TIMEOUT
from constants import RestApiDef, get_biz_http_status
from core.logger import get_logger

logger = get_logger("rest_client")


# 默认请求头：统一为 JSON 接口
DEFAULT_HEADERS = {"Content-Type": "application/json"}


class RestClient:
    """REST 请求封装，支持 session、统一 base_url 与超时。默认 Content-Type: application/json。"""

    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = (base_url or REST_BASE_URL).rstrip("/")
        self.timeout = timeout or REST_TIMEOUT
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    def _url(self, path: str) -> str:
        path = path if path.startswith("http") else f"{self.base_url}/{path.lstrip('/')}"
        return path

    def _request(
        self,
        method: str,
        path: str,
        **kwargs,
    ) -> requests.Response:
        url = self._url(path)
        kwargs.setdefault("timeout", self.timeout)
        # 入参、响应各打一行log，不截断，便于定位
        params = kwargs.get("params")
        body = kwargs.get("json") or kwargs.get("data")
        logger.info("[请求入参] %s %s | params=%s | body=%s", method.upper(), url, params, body)
        with allure.step(f"REST {method.upper()} {url}"):
            resp = self.session.request(method, url, **kwargs)
            resp_body = resp.text if resp.text else "(empty)"
            logger.info("[响应信息] status=%s | body=%s", resp.status_code, resp_body)
            allure.attach(
                resp_body,
                name="Response Body",
                attachment_type=allure.attachment_type.TEXT,
            )
            return resp

    # 未被引用，已注释
    # def get(self, path: str, **kwargs) -> requests.Response:
    #     return self._request("GET", path, **kwargs)

    def request(self, api: RestApiDef, params=None, json=None, **kwargs) -> requests.Response:
        """
        按 api.method 自动发起 GET/POST/PUT/PATCH/DELETE，使用 api.uri 作为 path。
        GET 常用 params，POST 常用 json，其余通过 **kwargs 传入。
        """
        kwargs.setdefault("params", params)
        kwargs.setdefault("json", json)
        return self._request(api.method.upper(), api.uri, **kwargs)

    def request_json_success(
        self,
        api: RestApiDef,
        expected_biz_code: int = 0,
        params=None,
        json=None,
        **kwargs,
    ) -> dict:
        """
        按 api.method 发起请求，并校验 HTTP 状态与 body 业务码符合 expected_biz_code，通过后返回响应 JSON。
        用例中无需再写 assert status_code、assert code，直接对返回的 data 做业务断言即可。
        """
        with allure.step(f"请求 {api.method.upper()} {api.uri} 并校验成功 (expected_biz_code={expected_biz_code})"):
            resp = self.request(api, params=params, json=json, **kwargs)
            with allure.step("校验 HTTP 状态码符合 expected_biz_code 映射"):
                expected_http = get_biz_http_status(expected_biz_code)
                assert resp.status_code == expected_http, (
                    f"HTTP status expected {expected_http}, got {resp.status_code}"
                )
            with allure.step("校验响应 body 中 code/biz_code"):
                data = resp.json()
                actual = data.get("biz_code", data.get("code"))
                assert actual == expected_biz_code, (
                    f"body code/biz_code expected {expected_biz_code}, got {actual}"
                )
            return data
