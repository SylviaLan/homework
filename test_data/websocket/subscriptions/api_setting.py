"""
WebSocket Subscriptions 接口定义。

包含订阅频道：
- book.{instrument_name}.{depth}: 订单簿
- ticker.{instrument_name}: 行情（待添加）
- trade.{instrument_name}: 成交（待添加）
- candlestick.{time_frame}.{instrument_name}: K 线（待添加）
"""
from constants import WsApiDef


# ==================== book 订阅 ====================

API_BOOK_SUBSCRIBE = WsApiDef(
    method="subscribe",
    request_params_example={"channels": ["book.BTCUSD-PERP.10"]},
    response_example={
        "code": 0,
        "method": "subscribe",
        "id": -1,
        "result": {
            "instrument_name": "BTCUSD-PERP",
            "subscription": "book.BTCUSD-PERP.10",
            "channel": "book",
            "depth": 10,
            "data": [{
                "asks": ["30082.5", "0.1689", "1"],
                "bids": ["30077.5", "1.0527", "2"],
                "u": 0, "tt": 0, "t": 0, "cs": 0,
            }],
        },
    },
    param_cases=None,  # param_cases 在 api_data.py 中定义并注入
)
