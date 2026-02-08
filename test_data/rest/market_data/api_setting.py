"""
Reference and Market Data API 接口定义。

包含接口：
- public/get-candlestick: K 线数据
- public/get-ticker: 行情数据（待添加）
- public/get-instruments: 合约信息（待添加）
"""
from constants import RestApiDef


# ==================== get-candlestick ====================

API_GET_CANDLESTICK = RestApiDef(
    uri="public/get-candlestick",
    method="get",
    request_params_example={
        "instrument_name": "BTCUSD-PERP",
        "timeframe": "M1",
        "count": 25,
        "start_ts": 0,
        "end_ts": 0,
    },
    response_example={
        "code": 0,
        "result": {
            "interval": "1m",
            "instrument_name": "BTCUSD-PERP",
            "data": [
                {"o": "0", "h": "0", "l": "0", "c": "0", "v": "0", "t": 0},
            ],
        },
    },
    param_cases=None,  # param_cases 在 api_data.py 中定义并注入
)
