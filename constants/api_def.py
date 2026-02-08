"""
REST / WebSocket 接口定义：与用例分离，支持多维度 param_cases 参数化。
- RestApiDef: uri + method，供 RestClient 使用。
- WsApiDef: method，供 WebSocket 订阅等；可选入参/出参示例、param_cases。
  WebSocket URL 不在此处定义，由 fixture（websocket_market_client / websocket_user_client）决定连接端点。
"""
from dataclasses import dataclass
from typing import Any, Literal, Optional


@dataclass(frozen=True)
class WsApiDef:
    """
    WebSocket 单条接口定义：method 以及可选的入参/出参示例与多维度参数化用例。
    - method: 如 "subscribe"
    - request_params_example / response_example: 仅作说明与参考
    - param_cases: 多维度参数化用例，形如 {"维度名": [case_dict, ...]}，供 get_param_cases(dimension) 使用
    注：WebSocket URL（market / user）由 pytest fixture 管理，不在此定义。
    """

    method: str = "subscribe"
    request_params_example: Optional[dict[str, Any]] = None
    response_example: Optional[dict[str, Any]] = None
    param_cases: Optional[dict[str, list[dict[str, Any]]]] = None

    def get_param_cases(self, dimension: str) -> list[dict[str, Any]]:
        """按维度名取参数化用例列表，无该维度或 param_cases 为空时返回 []。"""
        if not self.param_cases:
            return []
        return self.param_cases.get(dimension, [])


@dataclass(frozen=True)
class RestApiDef:
    """
    单条接口定义：uri、method，以及可选的入参/出参基本示例。
    - request_params_example: 入参示例（GET 为 query 键值，POST 可为 body 片段），仅作说明与参考。
    - response_example: 出参基本示例（如 code、result 结构），仅作说明与参考。
    - param_cases: 多维度参数化用例。形如 {"维度名": [case_dict, ...], ...}，例如 {"timeframe": [...], "instrument": [...]}。
      每个维度对应一组可 parametrize 的 case，case_dict 结构由该维度用例自行约定，供 pytest.mark.parametrize 等使用。
    """

    uri: str
    method: Literal["get", "post", "put", "patch", "delete"] = "get"
    request_params_example: Optional[dict[str, Any]] = None
    response_example: Optional[dict[str, Any]] = None
    param_cases: Optional[dict[str, list[dict[str, Any]]]] = None

    def get_param_cases(self, dimension: str) -> list[dict[str, Any]]:
        """按维度名取参数化用例列表，无该维度或 param_cases 为空时返回 []。"""
        if not self.param_cases:
            return []
        return self.param_cases.get(dimension, [])
