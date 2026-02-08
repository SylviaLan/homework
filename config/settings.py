"""
全局配置：环境变量、基础 URL、超时等。
REST_BASE_URL、WS_MARKET_URL、WS_USER_URL 根据环境（ENV）取值，也可用环境变量覆盖。
"""
import os

# 环境：test/uat / staging / prod
ENV = os.getenv("TEST_ENV", "uat").lower()

# 按环境配置的默认 base url
# REST 格式: {rest_base}/{method}  例: https://uat-api.3ona.co/exchange/v1/orders
# WebSocket 格式: 区分 market（行情）和 user（用户）两个端点
ENV_URLS = {
    "test": {
        "rest": "https://httpbin.org",
        "ws_market": "wss://echo.websocket.org",
        "ws_user": "wss://echo.websocket.org",
    },
    "uat": {
        "rest": "https://uat-api.3ona.co/exchange/v1",
        "ws_market": "wss://uat-stream.3ona.co/exchange/v1/market",
        "ws_user": "wss://uat-stream.3ona.co/exchange/v1/user",
    },
    "staging": {
        "rest": "https://staging-api.3ona.co/exchange/v1",
        "ws_market": "wss://uat-stream.3ona.co/exchange/v1/market",
        "ws_user": "wss://uat-stream.3ona.co/exchange/v1/user",
    },
    "prod": {
        "rest": "https://api.crypto.com/exchange/v1",
        "ws_market": "wss://stream.crypto.com/exchange/v1/market",
        "ws_user": "wss://stream.crypto.com/exchange/v1/user",
    },
}

# 按环境配置的 WebSocket 鉴权（与 ENV_URLS 分离，便于维护）
ENV_WS_CREDENTIALS = {
    "test": {"api_key": "", "secret_key": ""},
    "uat": {"api_key": "API_KEY", "secret_key": "SECRET_KEY"},
    "staging": {"api_key": "", "secret_key": ""},
    "prod": {"api_key": "", "secret_key": ""},
}

# 优先用环境变量，否则根据 ENV 取配置
_env_config = ENV_URLS.get(ENV, ENV_URLS["test"])
_ws_creds = ENV_WS_CREDENTIALS.get(ENV, ENV_WS_CREDENTIALS["test"])
REST_BASE_URL = os.getenv("REST_BASE_URL") or _env_config["rest"]
WS_MARKET_URL = os.getenv("WS_MARKET_URL") or _env_config["ws_market"]
WS_USER_URL = os.getenv("WS_USER_URL") or _env_config["ws_user"]
# 兼容旧代码：WS_BASE_URL 指向 market（后续可移除）
WS_BASE_URL = WS_MARKET_URL
WS_API_KEY = os.getenv("WS_API_KEY") or _ws_creds["api_key"]
WS_SECRET_KEY = os.getenv("WS_SECRET_KEY") or _ws_creds["secret_key"]

# REST API 超时
REST_TIMEOUT = int(os.getenv("REST_TIMEOUT", "10"))

# WebSocket 超时
WS_TIMEOUT = int(os.getenv("WS_TIMEOUT", "10"))

# 日志
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = os.getenv("LOG_DIR", "logs")
