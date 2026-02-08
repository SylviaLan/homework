"""
统一日志：控制台 + 文件，关键步骤打印，便于排查与 Allure 结合
"""
import logging
import os
import sys
from datetime import datetime

from config.settings import LOG_LEVEL, LOG_DIR


def get_logger(name: str = None) -> logging.Logger:
    """获取 logger，同名返回同一实例。"""
    logger = logging.getLogger(name or "auto_test")
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    # 不向 root 传播，避免与 pytest log_cli 重复输出（同一条日志只由本 logger 的 handler 打一次）
    logger.propagate = False
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # 文件：按日期分文件
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, f"test_{datetime.now().strftime('%Y%m%d')}.log")
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


# 框架默认 logger（当前未被引用，已注释）
# logger = get_logger("framework")
