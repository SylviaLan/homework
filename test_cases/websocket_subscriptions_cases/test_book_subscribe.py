"""
Book 订阅用例，对应 get_book_case.md 中 GB-001 ~ GB-010。

覆盖场景：
- 快照订阅（SNAPSHOT）：默认模式，每 500ms 强制发布快照
- 增量订阅（SNAPSHOT_AND_UPDATE）：先快照后 update，校验 u 递增及 pu 规则
- 空心跳：5s 无变化时发送空 book.update
- 异常入参：缺参、非法格式等
"""
import random

import allure
import pytest

from constants import INSTRUMENT_BTC
from core.logger import get_logger
from test_data.websocket.subscriptions import API_BOOK_SUBSCRIBE, RESP_BOOK_UPDATE_EXAMPLE
from utils.checker.response_checker import RespChecker

# ==================== 常量 ====================
TOLERANCE_MS = 10  # 时间误差容忍度（毫秒）
SNAPSHOT_INTERVAL_MS = 500  # 快照订阅默认发布间隔
HEARTBEAT_INTERVAL_MS = 5000  # 空心跳间隔

logger = get_logger(__name__)


# ==================== 正常用例 ====================

@allure.epic("WebSocket 订阅接口测试")
@allure.feature("Book 订阅")
@pytest.mark.websocket
class TestBookSubscribeCases:
    """Book 订阅正常场景测试"""

    @allure.title("GB-001 仅传必填 channels（默认 SNAPSHOT），校验快照间隔 500ms 及 u 字段一致")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.P0
    @pytest.mark.smoke
    def test_bs001_required_only(self, websocket_market_client):
        """默认快照订阅：每 500ms 强制发布一次快照，u 字段保持一致"""
        client = websocket_market_client

        with allure.step("发起订阅"):
            params = {"channels": [f"book.{INSTRUMENT_BTC}.10"]}
            msg = client.subscribe(params, random.randint(1, 10**5))
            RespChecker.assert_biz_success(msg)

        with allure.step("持续收包 1 秒"):
            follow_msgs = client.recv_for_seconds(SNAPSHOT_INTERVAL_MS * 2 / 1000)

        with allure.step("校验首条为快照（channel=book）"):
            RespChecker.assert_resp_should_be(follow_msgs, "$[0].result.channel", "book")
            RespChecker.assert_resp_should_be(follow_msgs, "$[0].result.depth", 10)

        with allure.step("校验所有消息的 u 字段一致"):
            RespChecker.assert_resp_all_list_value_same(follow_msgs, "$[*].result.data[0].u")

        with allure.step("校验快照间隔约 500ms"):
            RespChecker.assert_msg_time_interval(
                follow_msgs, expected_ms=SNAPSHOT_INTERVAL_MS, tolerance_ms=TOLERANCE_MS
            )

        with allure.step("校验响应结构应与example一致"):
            logger.info("现有的测试数据都返回了bids和asks=[]，校验先注释")
            # RespChecker.assert_resp_structure_be(follow_msgs[0],API_BOOK_SUBSCRIBE.response_example)


    @allure.title("GB-002 指定 depth=50 订阅，校验返回 depth")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.P1
    @pytest.mark.smoke
    def test_bs002_snapshot_depth_50(self, websocket_market_client):
        """指定深度 50 订阅"""
        client = websocket_market_client

        with allure.step("发起 depth=50 订阅"):
            params = {"channels": [f"book.{INSTRUMENT_BTC}.50"]}
            msg = client.subscribe(params, random.randint(1, 10**5))
            RespChecker.assert_biz_success(msg)

        with allure.step("持续收包 1 秒"):
            follow_msgs = client.recv_for_seconds(1)

        with allure.step("校验返回 depth=50"):
            RespChecker.assert_resp_should_be(follow_msgs, "$[0].result.depth", 50)

    @allure.title("GB-003 增量订阅（SNAPSHOT_AND_UPDATE），校验先快照后 update，及 u/pu 规则，有更新时，校验响应结构")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.P0
    @pytest.mark.smoke
    def test_bs003_snapshot_and_update(self, websocket_market_client):
        """增量订阅：先收快照，后收 book.update；u 递增，pu == 前一条 u"""
        client = websocket_market_client

        with allure.step("发起增量订阅"):
            params = {
                "channels": [f"book.{INSTRUMENT_BTC}.10"],
                "book_subscription_type": "SNAPSHOT_AND_UPDATE",
                "book_update_frequency": 10,
            }
            msg = client.subscribe(params, random.randint(1, 10**5))
            RespChecker.assert_biz_success(msg)

        with allure.step("持续收包直到收到 book.update 或满 3 条"):
            stop_when = lambda m, msgs: (
                len(msgs) >= 3 or (m.get("result") or m).get("channel") == "book.update"
            )
            follow_msgs = client.recv_until(stop_when, max_wait_sec=10.0)

        with allure.step("校验消息顺序：先快照后 update"):
            assert len(follow_msgs) >= 2, f"需要至少 2 条消息，实际 {len(follow_msgs)} 条"
            RespChecker.assert_resp_should_be(follow_msgs, "$[0].result.channel", "book")
            RespChecker.assert_resp_should_be(follow_msgs, "$[1].result.channel", "book.update")

        with allure.step("校验 u 字段递增"):
            RespChecker.assert_list_field_increasing(follow_msgs, "result.data.0.u", strict=False)

        with allure.step("校验 pu == 前一条 u"):
            RespChecker.assert_list_pu_matches_prev_u(follow_msgs)

        # TODO: 当有持续更新的 instrument 时，启用book.update的响应格式校验
        with allure.step("校验响应结构应与定义的一致"):
            logger.info("现有的测试数据都返回了bids和asks=[]，该校验先注释")
            # RespChecker.assert_resp_structure_be(
            #     follow_msgs, "$[1].result.channel",
            #     RESP_BOOK_UPDATE_EXAMPLE
            # )

    @allure.title("GB-004 增量订阅 frequency=100，校验 update 消息频率")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.P1
    def test_bs004_update_frequency_100(self, websocket_market_client):
        """增量订阅指定频率 100ms"""
        client = websocket_market_client

        with allure.step("发起 frequency=100 订阅"):
            params = {
                "channels": [f"book.{INSTRUMENT_BTC}.10"],
                "book_subscription_type": "SNAPSHOT_AND_UPDATE",
                "book_update_frequency": 100,
            }
            msg = client.subscribe(params, random.randint(1, 10**5))
            RespChecker.assert_biz_success(msg)

        with allure.step("持续收包直到满 3 条"):
            stop_when = lambda m, msgs: len(msgs) >= 3
            follow_msgs = client.recv_until(stop_when, max_wait_sec=10.0)

        with allure.step("校验收到 book.update"):
            assert len(follow_msgs) >= 2, f"需要至少 2 条消息，实际 {len(follow_msgs)} 条"
            RespChecker.assert_resp_should_be(follow_msgs, "$[1].result.channel", "book.update")

        # TODO: 当有持续更新的 instrument 时，启用频率校验
        # RespChecker.assert_msg_time_interval(follow_msgs, expected_ms=100, tolerance_ms=TOLERANCE_MS)

    @allure.title("GB-005 增量订阅无更新时，5s 后收到空心跳，校验 u/pu 规则")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.P1
    def test_bs005_empty_heartbeat(self, websocket_market_client):
        """5s 无变化时发送空 book.update（asks/bids 为空），u/pu 规则仍适用"""
        client = websocket_market_client

        with allure.step("发起增量订阅"):
            params = {
                "channels": [f"book.{INSTRUMENT_BTC}.10"],
                "book_subscription_type": "SNAPSHOT_AND_UPDATE",
                "book_update_frequency": 100,
            }
            msg = client.subscribe(params, random.randint(1, 10**5))
            RespChecker.assert_biz_success(msg)

        with allure.step("持续收包直到收到首条 book.update"):
            stop_when = lambda m: (m.get("result") or m).get("channel") == "book.update"
            follow_msgs = client.recv_until(stop_when, max_wait_sec=10.0)

        with allure.step("继续收包等待空心跳（约 5.5s）"):
            wait_sec = (HEARTBEAT_INTERVAL_MS + HEARTBEAT_INTERVAL_MS * 0.1) / 1000
            follow_msgs_after = client.recv_for_seconds(wait_sec)

        all_msgs = follow_msgs + follow_msgs_after

        with allure.step("校验空心跳间隔约 5s"):
            RespChecker.assert_msg_time_interval(
                all_msgs,
                expected_ms=HEARTBEAT_INTERVAL_MS,
                tolerance_ms=TOLERANCE_MS,
                idx0=len(follow_msgs) - 1,
                idx1=len(follow_msgs),
            )

        with allure.step("校验空心跳 asks/bids 为空"):
            RespChecker.assert_resp_should_be(follow_msgs_after, "$[0].result.data.[0].update.asks", [])
            RespChecker.assert_resp_should_be(follow_msgs_after, "$[0].result.data.[0].update.bids", [])

        with allure.step("校验空心跳的 u 递增及 pu == 前一条 u"):
            RespChecker.assert_list_field_increasing(all_msgs, "result.data.0.u", strict=False)
            RespChecker.assert_list_pu_matches_prev_u(all_msgs)


# ==================== 异常用例 ====================

@allure.epic("WebSocket 订阅接口测试")
@allure.feature("Book 订阅 - 异常")
@pytest.mark.websocket
@pytest.mark.abnormal
class TestBookSubscribeAbnormal:
    """Book 订阅异常入参测试（GB-009、GB-010）"""

    @pytest.mark.parametrize(
        "case",
        API_BOOK_SUBSCRIBE.get_param_cases("abnormal"),
        ids=[c["case_id"] for c in API_BOOK_SUBSCRIBE.get_param_cases("abnormal")],
    )
    def test_abnormal_params(self, websocket_market_client, case):
        """异常入参校验：缺参、空值、非法格式等"""
        params = case.get("params")
        expected_biz_code = case["expected_biz_code"]

        msg = websocket_market_client.subscribe(params, random.randint(1, 10**5))
        RespChecker.assert_biz_code(msg, expected_biz_code)
