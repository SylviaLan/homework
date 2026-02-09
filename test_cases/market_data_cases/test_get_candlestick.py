"""
get-candlestick 用例对应 get_candles_case.md 中 GC-001 ~ GC-015。
使用 RespChecker 进行响应校验，支持 jsonpath 取值、结构比较、范围校验等。
"""
import time
import allure
import pytest

from constants import BizCode, get_biz_http_status, INSTRUMENT_BTC, INSTRUMENT_ETH
from test_data.rest.market_data import API_GET_CANDLESTICK
from utils.checker.response_checker import RespChecker

# 时间相关常量
DAY_MS = 24 * 3600 * 1000


@allure.epic("行情数据用例")
@allure.feature("获取行情/K线数据")
@pytest.mark.rest
class TestGetCandlestick:
    """public/get-candlestick 自动化用例，对应 get_candles_case.md。"""

    @allure.title("GC-001 仅传必填参数 instrument_name，校验默认值与响应结构")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.P0
    def test_gc001_required_only(self, rest_client):
        data = rest_client.request_json_success(API_GET_CANDLESTICK, params={"instrument_name": INSTRUMENT_BTC})

        # 响应结构校验
        RespChecker.assert_resp_structure_be(data.get("result"), API_GET_CANDLESTICK.response_example.get("result"))

        # 默认值校验
        RespChecker.assert_resp_should_be(data, "$.result.interval", "1m")

        # 默认 count 校验
        RespChecker.assert_resp_length_lte(data, "$.result.data", 25)

        # 时间范围校验
        now_ms = int(time.time() * 1000)
        RespChecker.assert_resp_all_in_range(data, "$.result.data[*].t", now_ms - 2 * DAY_MS, now_ms + 60000)

    @allure.title("GC-002~005 指定 timeframe 获取 K 线，校验 K 的时间间隔")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.P0
    @pytest.mark.parametrize(
        "case",
        API_GET_CANDLESTICK.get_param_cases("timeframe"),
        ids=[c["timeframe"] for c in API_GET_CANDLESTICK.get_param_cases("timeframe")],
    )
    def test_gc002_to_gc005_timeframe(self, rest_client, case):
        data = rest_client.request_json_success(
            API_GET_CANDLESTICK,
            params={"instrument_name": INSTRUMENT_BTC, "timeframe": case["timeframe"]},
        )
        # 校验 interval
        RespChecker.assert_resp_should_be(data, "$.result.interval", case["expected_interval"])

        # 校验 K 线时间步长
        if "interval_ms_min" in case and "interval_ms_max" in case:
            RespChecker.assert_list_time_step(
                data, "$.result.data", time_field="t",
                min_ms=case["interval_ms_min"], max_ms=case["interval_ms_max"]
            )
        else:
            RespChecker.assert_list_time_step(
                data, "$.result.data", time_field="t", expected_ms=case["interval_ms"]
            )

    @allure.title("GC-006 指定 count 条数，校验返回条数 <= count")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.P1
    def test_gc006_count(self, rest_client):
        data = rest_client.request_json_success(
            API_GET_CANDLESTICK,
            params={"instrument_name": INSTRUMENT_BTC, "count": 10},
        )
        RespChecker.assert_resp_length_lte(data, "$.result.data", 10)

    @allure.title("GC-007 指定 start_ts 与 end_ts，校验 t 在范围内")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.P1
    def test_gc007_start_end_ts(self, rest_client):
        now_ms = int(time.time() * 1000)
        start_ts, end_ts = now_ms - DAY_MS, now_ms
        data = rest_client.request_json_success(
            API_GET_CANDLESTICK,
            params={"instrument_name": INSTRUMENT_BTC, "start_ts": start_ts, "end_ts": end_ts},
        )
        RespChecker.assert_resp_all_in_range(data, "$.result.data[*].t", start_ts, end_ts)

    @allure.title("GC-008 全参数，校验返回数据与参数一致")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.P1
    def test_gc008_full_params(self, rest_client):
        now_ms = int(time.time() * 1000)
        start_ts, end_ts = now_ms - DAY_MS, now_ms
        params = {
            "instrument_name": INSTRUMENT_BTC,
            "timeframe": "M15",
            "count": 20,
            "start_ts": start_ts,
            "end_ts": end_ts,
        }
        data = rest_client.request_json_success(API_GET_CANDLESTICK, params=params)

        RespChecker.assert_resp_should_be(data, "$.result.interval", "M15")
        RespChecker.assert_resp_length_lte(data, "$.result.data", 20)

    @allure.title("GC-009 不同合约 instrument_name，校验返回一致")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.P2
    def test_gc009_other_instrument(self, rest_client):
        data = rest_client.request_json_success(
            API_GET_CANDLESTICK,
            params={"instrument_name": INSTRUMENT_ETH},
        )
        RespChecker.assert_resp_should_be(data, "$.result.instrument_name", INSTRUMENT_ETH)


# ==================== 异常用例 ====================

@allure.epic("行情数据用例")
@allure.feature("获取行情/K线数据 - 异常")
@pytest.mark.rest
@pytest.mark.abnormal
class TestGetCandlestickAbnormal:
    """public/get-candlestick 异常入参测试（GC-010 ~ GC-015）"""

    @allure.title("GC-010~012 异常 instrument_name（缺参/空串/非法），校验 HTTP 与 biz_code")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.P1
    @pytest.mark.parametrize(
        "case",
        API_GET_CANDLESTICK.get_param_cases("abnormal_instrument"),
        ids=[c["case_id"] for c in API_GET_CANDLESTICK.get_param_cases("abnormal_instrument")],
    )
    def test_gc010_to_gc012_abnormal_instrument(self, rest_client, case):
        params = case.get("params")
        resp = rest_client.request(API_GET_CANDLESTICK, params=params)
        expected_biz_code = case["expected_biz_code"]

        RespChecker.assert_http_status(resp, get_biz_http_status(expected_biz_code))
        RespChecker.assert_biz_code(resp.json(), expected_biz_code)

    @allure.title("GC-013 timeframe 非法值，应报错")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.P2
    def test_gc013_invalid_timeframe(self, rest_client):
        resp = rest_client.request(
            API_GET_CANDLESTICK,
            params={"instrument_name": INSTRUMENT_BTC, "timeframe": "INVALID"},
        )
        RespChecker.assert_biz_code(resp.json(), BizCode.INVALID_REQUEST)

    @allure.title("GC-015 start_ts > end_ts，成功时应返回空列表")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.P2
    def test_gc015_start_gt_end(self, rest_client):
        now_ms = int(time.time() * 1000)
        params = {"instrument_name": INSTRUMENT_BTC, "start_ts": now_ms, "end_ts": now_ms - DAY_MS}
        resp = rest_client.request(API_GET_CANDLESTICK, params=params)
        data = resp.json()

        if data.get("code") == BizCode.SUCCESS:
            RespChecker.assert_resp_length_should_be(data, "$.result.data", 0)
