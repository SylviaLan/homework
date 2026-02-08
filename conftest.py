"""
pytest 全局配置：fixtures、日志初始化、Allure 环境信息
"""
import os

import pytest

from config.settings import WS_MARKET_URL, WS_USER_URL
from core.logger import get_logger
from core.rest_client import RestClient
from core.websocket_client import WebSocketClient

logger = get_logger("conftest")


@pytest.fixture(scope="session")
def rest_client():
    """Session 级 REST 客户端，复用连接。"""
    logger.info("Create session REST client")
    client = RestClient()
    yield client
    logger.info("Session end, REST client closed")


@pytest.fixture
def websocket_market_client():
    """
    用例级 WebSocket Market 客户端（行情订阅：book、ticker 等）。
    URL: wss://uat-stream.3ona.co/exchange/v1/market
    fixture 负责连接和关闭，用例直接使用即可。
    """
    logger.info("Create and connect WebSocket market client: %s", WS_MARKET_URL)
    client = WebSocketClient(url=WS_MARKET_URL)
    client.connect()  # fixture 中建立连接
    yield client
    client.close()
    logger.info("WebSocket market client closed")


@pytest.fixture
def websocket_user_client():
    """
    用例级 WebSocket User 客户端（用户相关：订单、账户等，需鉴权）。
    URL: wss://uat-stream.3ona.co/exchange/v1/user
    fixture 负责连接和关闭，用例直接使用即可。
    """
    logger.info("Create and connect WebSocket user client: %s", WS_USER_URL)
    client = WebSocketClient(url=WS_USER_URL)
    client.connect()  # fixture 中建立连接
    yield client
    client.close()
    logger.info("WebSocket user client closed")


def pytest_configure(config):
    """Allure 环境信息写入。"""
    allure_dir = "reports/allure-results"
    os.makedirs(allure_dir, exist_ok=True)
    env_path = os.path.join(allure_dir, "environment.properties")
    with open(env_path, "w", encoding="utf-8") as f:
        f.write("env=test\n")
        f.write("framework=pytest\n")
