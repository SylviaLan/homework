"""
WebSocket 客户端封装：连接、发送、接收、关闭，带超时与日志。
支持原始 send/recv 与 JSON 格式 send_json/recv_json，及 book 订阅请求构造。
支持通用持续收包：recv_until(stop_when, max_wait_sec) 按可传入的终止条件收包；recv_for_seconds(duration_sec) 按时长收包。
User API 需在会话内调用一次 public/auth（带 sig + api_key），鉴权后本会话内后续请求无需再带签名。
"""
import inspect
import json
import socket
import time
from typing import Callable, Union

import allure
import websocket

from config.settings import WS_BASE_URL, WS_TIMEOUT, WS_API_KEY, WS_SECRET_KEY
from core.logger import get_logger
from core.ws_signature import build_signed_request, build_signed_subscribe

logger = get_logger("websocket_client")

# User API 鉴权 method，每个会话调用一次
WS_AUTH_METHOD = "public/auth"


class WebSocketClient:
    """WebSocket 封装：connect / send / recv / close，支持 JSON 与 book 订阅。"""

    def __init__(self, url: str = None, timeout: int = None):
        self.url = url or WS_BASE_URL
        self.timeout = timeout or WS_TIMEOUT
        self._ws = None

    def connect(self) -> "WebSocketClient":
        """建立连接（如已连接则跳过）。"""
        if self._ws is not None:
            logger.info("WebSocket already connected, skip connect")
            return self
        logger.info("WebSocket connecting to %s", self.url)
        with allure.step(f"WebSocket connect: {self.url}"):
            self._ws = websocket.create_connection(self.url, timeout=self.timeout)
            logger.info("WebSocket connected")
            return self

    def send(self, payload: str | bytes) -> None:
        """发送原始消息。"""
        logger.info("WebSocket send: %s", payload[:200] if len(str(payload)) > 200 else payload)
        with allure.step("WebSocket send"):
            allure.attach(
                str(payload)[:1000],
                name="Sent",
                attachment_type=allure.attachment_type.TEXT,
            )
            self._ws.send(payload)

    def send_json(self, obj: dict) -> None:
        """发送 JSON 对象（自动序列化）。"""
        raw = json.dumps(obj)
        self.send(raw)

    def recv(self) -> str | bytes:
        """接收一条消息，阻塞直到有数据或超时。"""
        out = self._ws.recv()
        logger.info("WebSocket recv: %s", out[:200] if len(str(out)) > 200 else out)
        with allure.step("WebSocket recv"):
            allure.attach(
                str(out)[:1000],
                name="Received",
                attachment_type=allure.attachment_type.TEXT,
            )
            return out

    def recv_json(self) -> dict:
        """接收一条消息并解析为 JSON。"""
        out = self.recv()
        text = out.decode("utf-8") if isinstance(out, bytes) else out
        return json.loads(text)

    def recv_until(
        self,
        stop_when: Union[Callable[[dict], bool], Callable[[dict, list], bool], None],
        max_wait_sec: float,
        recv_timeout: float = 1.0,
        filter_heartbeat: bool = True,
    ) -> list:
        """
        在 max_wait_sec 内持续接收消息，直到 stop_when 返回 True 或超时。
        :param stop_when: 终止条件，支持两种签名：
                          - stop_when(msg) -> bool: 仅判断当前消息
                          - stop_when(msg, messages) -> bool: 可获取已收消息列表（用于判断消息数量等）
                          None 表示不设条件，仅按超时结束
        :param max_wait_sec: 最大等待时间（秒）
        :param recv_timeout: 单次 recv 超时（秒），超时后继续循环
        :param filter_heartbeat: 是否自动过滤 heartbeat 消息（默认 True）
        :return: 收到的 JSON 消息列表（已过滤 heartbeat）
        """
        if not self._ws or not getattr(self._ws, "sock", None):
            logger.warning("recv_until: 未连接或无 sock，跳过")
            return []

        # 检测 stop_when 参数数量
        stop_when_takes_two_args = False
        if stop_when is not None:
            try:
                sig = inspect.signature(stop_when)
                stop_when_takes_two_args = len(sig.parameters) >= 2
            except (ValueError, TypeError):
                pass

        messages = []
        heartbeat_count = 0
        deadline = time.time() + max_wait_sec
        old_timeout = self._ws.sock.gettimeout()
        logger.info(
            "持续收包最多 %.1fs（单次 recv 超时 %.1fs，终止条件=%s，过滤heartbeat=%s）",
            max_wait_sec,
            recv_timeout,
            "有" if stop_when else "无（仅超时）",
            filter_heartbeat,
        )
        try:
            self._ws.sock.settimeout(recv_timeout)
            while time.time() < deadline:
                try:
                    raw = self._ws.recv()
                    text = raw.decode("utf-8") if isinstance(raw, bytes) else raw
                    msg = json.loads(text)

                    # 过滤 heartbeat
                    if filter_heartbeat and self.is_heartbeat(msg):
                        heartbeat_count += 1
                        logger.debug("跳过 heartbeat 消息 [%d]", heartbeat_count)
                        continue

                    messages.append(msg)
                    preview = text if len(text) <= 500 else text[:500] + "..."
                    logger.info("WebSocket 持续收包 [%d] 收到: %s", len(messages), preview)

                    # 调用 stop_when（兼容单参数和双参数）
                    if stop_when is not None:
                        should_stop = stop_when(msg, messages) if stop_when_takes_two_args else stop_when(msg)
                        if should_stop:
                            logger.info("满足终止条件，结束收包")
                            break
                except socket.timeout:
                    continue
                except Exception as e:
                    if "timeout" in str(type(e).__name__).lower() or "timed out" in str(e).lower():
                        continue
                    raise
        finally:
            self._ws.sock.settimeout(old_timeout)
        if heartbeat_count > 0:
            logger.info("持续收包结束，共收到 %d 条业务消息（已过滤 %d 条 heartbeat）", len(messages), heartbeat_count)
        else:
            logger.info("持续收包结束，共收到 %d 条消息", len(messages))
        return messages

    def recv_for_seconds(
        self, duration_sec: float, recv_timeout: float = 1.0, filter_heartbeat: bool = True
    ) -> list:
        """
        在指定时长内持续接收消息，无提前终止条件。
        :param duration_sec: 接收时长（秒）
        :param recv_timeout: 单次 recv 超时（秒）
        :param filter_heartbeat: 是否自动过滤 heartbeat 消息（默认 True）
        :return: 收到的 JSON 消息列表（已过滤 heartbeat）
        """
        return self.recv_until(None, duration_sec, recv_timeout, filter_heartbeat)

    def authenticate(self, api_key: str, secret_key: str, *, params: dict = None, request_id: int = 1) -> dict:
        """
        执行 public/auth 鉴权（每个会话调用一次）。
        请求体含 api_key、nonce、sig（HMAC-SHA256），鉴权成功后本会话内后续请求无需再带 sig/api_key。
        :return: 服务端响应（通常含 code、result 等），调用方可根据 code 判断是否成功。
        """
        req = build_signed_request(
            WS_AUTH_METHOD,
            api_key,
            secret_key,
            params=params or {},
            request_id=request_id,
        )
        logger.info("WebSocket auth: method=%s id=%s", WS_AUTH_METHOD, request_id)
        self.send_json(req)
        return self.recv_json()

    def subscribe(self, params: dict, request_id: int = 1) -> dict:
        """
        发送明文 subscribe 请求（无 auth/sig），并返回服务端响应。
        :param params: subscribe 的 params，如 {"channels": ["book.BTCUSD-PERP.10"], ...}
        :return: 服务端 JSON 响应（含 code、result 等）
        """
        payload = {"id": request_id, "method": "subscribe", "params": params}
        self.send_json(payload)
        return self.recv_json()

    def subscribe_signed(self, params: dict, request_id: int = 23) -> dict:
        """
        发送带签名的 subscribe 请求，并返回服务端响应。
        api_key、secret_key 从 config.settings 读取（按环境区分，可被环境变量覆盖）。
        :param params: 待测参数（subscribe 的 params），如 {"channels": ["book.BTCUSD-PERP.10"], ...}
        :return: 服务端 JSON 响应（含 code、result 等）
        """
        payload = build_signed_subscribe(params, WS_API_KEY, WS_SECRET_KEY, request_id=request_id)
        self.send_json(payload)
        return self.recv_json()

    def close(self) -> None:
        """关闭连接。"""
        if self._ws:
            logger.info("WebSocket closing")
            try:
                self._ws.close()
            except Exception as e:
                logger.warning("WebSocket close error: %s", e)
            self._ws = None

    # ========== 消息过滤工具方法 ==========

    @staticmethod
    def filter_heartbeat(msgs: list[dict]) -> list[dict]:
        """
        过滤掉 heartbeat 消息，返回业务消息列表。
        heartbeat 特征：method == "public/heartbeat"
        Args:
            msgs: 原始消息列表
        Returns:
            过滤后的消息列表（不含 heartbeat）
        """
        return [m for m in msgs if m.get("method") != "public/heartbeat"]

    @staticmethod
    def is_heartbeat(msg: dict) -> bool:
        """判断消息是否为 heartbeat。"""
        return msg.get("method") == "public/heartbeat"

    def __enter__(self) -> "WebSocketClient":
        return self.connect()

    def __exit__(self, *args):
        self.close()
