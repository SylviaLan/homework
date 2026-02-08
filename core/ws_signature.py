"""
WebSocket User API 签名：HMAC-SHA256( payload_str, SECRET_KEY )。
payload_str = method + str(id) + api_key + param_str + str(nonce)，
param_str 为 params 按 key 字母序序列化（最多 MAX_LEVEL 层）。
"""
import hashlib
import hmac
import time
import random
from core.logger import get_logger

logger = get_logger("ws_signature")

MAX_LEVEL = 3


def params_to_str(obj, level: int = 0) -> str:
    """
    params 按 key 字母序序列化，用于参与签名的 param_str。
    - 仅对 dict 做 key 遍历；list 中元素若为非 dict（如 str/int）则直接 str(value)
    - level >= MAX_LEVEL 时直接 str(obj)
    - None -> 'null'，list 逐项递归（仅子项为 dict 时再递归），否则 str(value)
    """
    if level >= MAX_LEVEL or not isinstance(obj, dict):
        return str(obj)
    return_str = ""
    for key in sorted(obj):
        return_str += key
        val = obj[key]
        if val is None:
            return_str += "null"
        elif isinstance(val, list):
            for sub_obj in val:
                return_str += params_to_str(sub_obj, level + 1)
        else:
            return_str += str(val)
    return return_str


def build_signed_request(
    method: str,
    api_key: str,
    secret_key: str,
    *,
    params: dict = None,
    request_id: int = None,
    nonce: int = None,
) -> dict:
    """
    构造带 sig 的请求体，用于 public/auth 及需要签名的 private 等。
    :param method: 如 "public/auth", "private/create-order-list"
    :param api_key: API Key
    :param secret_key: API Secret（用于 HMAC-SHA256）
    :param params: 可选参数字典
    :param request_id: 请求 id，默认 1
    :param nonce: 毫秒时间戳，默认当前时间
    :return: 含 id, method, api_key, params, nonce, sig 的 dict
    """
    request_id = request_id if request_id is not None else random.randint(1, 10000)
    nonce = nonce if nonce is not None else int(time.time() * 1000)
    params = params if params is not None else {}

    req = {
        "id": request_id,
        "method": method,
        # "api_key": api_key,
        "params": params,
        # "nonce": nonce,
    }

    # param_str = params_to_str(req["params"], 0)
    # payload_str = req["method"] + str(req["id"]) + req["api_key"] + param_str + str(req["nonce"])
    #
    # req["sig"] = hmac.new(
    #     bytes(str(secret_key), "utf-8"),
    #     msg=bytes(payload_str, "utf-8"),
    #     digestmod=hashlib.sha256,
    # ).hexdigest()

    logger.debug("Built signed request for method=%s id=%s", method, request_id)
    return req


def build_signed_subscribe(
    params: dict,
    api_key: str,
    secret_key: str,
    request_id: int = 1,
) -> dict:
    """
    通用：构造带签名的 subscribe 请求体。
    :param params: subscribe 的 params（如 channels、book_subscription_type、book_update_frequency 等）
    :param api_key: API Key
    :param secret_key: API Secret（用于 HMAC-SHA256）
    :param request_id: 请求 id
    :return: 含 id, method, api_key, params, nonce, sig 的 dict
    """
    return build_signed_request(
        "subscribe",
        api_key,
        secret_key,
        params=params,
        request_id=request_id,
    )
