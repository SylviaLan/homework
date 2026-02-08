"""
Reference and Market Data API 测试数据。

包含 DDT 参数化数据、响应示例等。
"""
from constants import INSTRUMENT_INVALID

from .api_setting import API_GET_CANDLESTICK


# ==================== 时间常量 ====================

_MS_MIN = 60 * 1000
_MS_HOUR = 3600 * 1000
_MS_DAY = 24 * _MS_HOUR
_INTERVAL_MS_1M_MIN = 28 * _MS_DAY
_INTERVAL_MS_1M_MAX = 31 * _MS_DAY


# ==================== GET_CANDLESTICK 测试数据 ====================

# GC-002 ~ GC-005: timeframe 参数化数据
CANDLESTICK_TIMEFRAME_CASES = [
    {"timeframe": "M1", "expected_interval": "M1", "interval_ms": 1 * _MS_MIN},
    {"timeframe": "M5", "expected_interval": "M5", "interval_ms": 5 * _MS_MIN},
    {"timeframe": "M15", "expected_interval": "M15", "interval_ms": 15 * _MS_MIN},
    {"timeframe": "M30", "expected_interval": "M30", "interval_ms": 30 * _MS_MIN},
    {"timeframe": "H1", "expected_interval": "H1", "interval_ms": 1 * _MS_HOUR},
    {"timeframe": "H2", "expected_interval": "H2", "interval_ms": 2 * _MS_HOUR},
    {"timeframe": "H4", "expected_interval": "H4", "interval_ms": 4 * _MS_HOUR},
    {"timeframe": "4h", "expected_interval": "4h", "interval_ms": 4 * _MS_HOUR},
    {"timeframe": "H12", "expected_interval": "H12", "interval_ms": 12 * _MS_HOUR},
    {"timeframe": "1D", "expected_interval": "1D", "interval_ms": _MS_DAY},
    {"timeframe": "D1", "expected_interval": "D1", "interval_ms": _MS_DAY},
    {"timeframe": "1d", "expected_interval": "1d", "interval_ms": _MS_DAY},
    {"timeframe": "7D", "expected_interval": "7D", "interval_ms": 7 * _MS_DAY},
    {"timeframe": "14D", "expected_interval": "14D", "interval_ms": 14 * _MS_DAY},
    {
        "timeframe": "1M",
        "expected_interval": "1M",
        "interval_ms": 30 * _MS_DAY,
        "interval_ms_min": _INTERVAL_MS_1M_MIN,
        "interval_ms_max": _INTERVAL_MS_1M_MAX,
    },
]

# GC-010 ~ GC-012: 异常 instrument_name 参数化数据
CANDLESTICK_ABNORMAL_INSTRUMENT_CASES = [
    {"case_id": "gc010_missing", "params": None, "expected_biz_code": 40003},
    {"case_id": "gc011_empty", "params": {"instrument_name": ""}, "expected_biz_code": 40004},
    {"case_id": "gc012_invalid", "params": {"instrument_name": INSTRUMENT_INVALID}, "expected_biz_code": 40004},
]


# ==================== 注入 param_cases 到 API 定义 ====================

object.__setattr__(API_GET_CANDLESTICK, "param_cases", {
    "timeframe": CANDLESTICK_TIMEFRAME_CASES,
    "abnormal_instrument": CANDLESTICK_ABNORMAL_INSTRUMENT_CASES,
})
