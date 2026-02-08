"""
WebSocket Subscriptions 测试数据。

包含 DDT 参数化数据、响应示例等。
"""
from .api_setting import API_BOOK_SUBSCRIBE


# ==================== BOOK_SUBSCRIBE 测试数据 ====================

# GB-009 ~ GB-010: 异常入参参数化数据
BOOK_SUBSCRIBE_ABNORMAL_CASES = [
    # GB-009: 缺参 / channels 为空
    {"case_id": "bs009_missing_channels", "params": {}, "expected_biz_code": 40003},
    {"case_id": "bs009_empty_channels", "params": {"channels": []}, "expected_biz_code": 40003},
    # GB-010: 非法 channel 格式
    {"case_id": "bs010_invalid_channel_format", "params": {"channels": ["invalid.channel"]}, "expected_biz_code": 40003},
    {"case_id": "bs010_channel_incomplete", "params": {"channels": ["book"]}, "expected_biz_code": 40003},
    {"case_id": "bs010_invalid_instrument", "params": {"channels": ["book.INVALID-INSTRUMENT.10"]}, "expected_biz_code": 40003},
    {"case_id": "bs010_invalid_depth", "params": {"channels": ["book.BTCUSD-PERP.999"]}, "expected_biz_code": 40003},
    {"case_id": "bs010_invalid_subscription_type", "params": {"channels": ["book.BTCUSD-PERP.10"], "book_subscription_type": "INVALID_TYPE"}, "expected_biz_code": 40003},
    {"case_id": "bs010_invalid_update_frequency", "params": {"channels": ["book.BTCUSD-PERP.10"], "book_update_frequency": 9999}, "expected_biz_code": 40003},
]

# book.update 增量响应示例（用于结构校验）
RESP_BOOK_UPDATE_EXAMPLE = {
    "id": -1,
    "method": "subscribe",
    "code": 0,
    "result": {
        "instrument_name": "BTCUSD-PERP",
        "subscription": "book.BTCUSD-PERP.50",
        "channel": "book.update",
        "depth": 50,
        "data": [{
            "update": {
                "asks": ["30082.5", "0.1689", "1"],
                "bids": ["30077.5", "1.0527", "2"],
            },
            "t": 0, "tt": 0, "u": 0, "pu": 0, "cs": 35,
        }],
    },
}


# ==================== 注入 param_cases 到 API 定义 ====================

object.__setattr__(API_BOOK_SUBSCRIBE, "param_cases", {
    "abnormal": BOOK_SUBSCRIBE_ABNORMAL_CASES,
})
