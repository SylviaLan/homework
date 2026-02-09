# 基于 Pytest 的接口自动化测试框架

支持 **REST** 与 **WebSocket** 两类接口：基础封装、用例与数据分离、Allure 报告与步骤、统一日志、业务码与结构校验。

## 项目结构

```
homework/
├── conftest.py                      # pytest 全局 fixture、Allure 环境配置
├── pytest.ini                       # 用例发现、markers、日志、Allure 配置
├── requirements.txt                 # 项目依赖
│
├── config/
│   └── settings.py                  # 环境配置（TEST_ENV、REST/WS URL、超时等）
│
├── constants/                       # 常量与类型定义
│   ├── __init__.py                  # 统一导出
│   ├── api_def.py                   # RestApiDef / WsApiDef 接口定义类
│   ├── biz_status.py                # BizCode 业务码、get_biz_http_status 映射
│   └── common.py                    # INSTRUMENT_BTC/ETH 等通用常量
│
├── core/                            # 核心封装
│   ├── logger.py                    # 统一日志（控制台 + 文件）
│   ├── rest_client.py               # REST 客户端（request / request_json_success）
│   ├── websocket_client.py          # WebSocket 客户端（connect / subscribe / recv_until）
│   └── ws_signature.py              # WebSocket 签名工具
│
├── utils/
│   └── checker/
│       └── response_checker.py      # RespChecker 响应校验工具类
│
├── test_data/                       # 测试数据（按业务模块组织）
│   ├── rest/
│   │   └── market_data/             # Reference and Market Data API
│   │       ├── __init__.py
│   │       ├── api_setting.py       # API_GET_CANDLESTICK 接口定义
│   │       └── api_data.py          # CANDLESTICK_*_CASES 参数化数据
│   └── websocket/
│       └── subscriptions/           # WebSocket Subscriptions
│           ├── __init__.py
│           ├── api_setting.py       # API_BOOK_SUBSCRIBE 接口定义
│           └── api_data.py          # BOOK_SUBSCRIBE_*_CASES、RESP_* 响应示例
│
├── test_cases/                      # 测试用例
│   ├── market_data_cases/
│   │   ├── get_candles_case.md      # 用例设计文档
│   │   └── test_get_candlestick.py  # K 线接口用例（GC-001 ~ GC-015）
│   └── websocket_subscriptions_cases/
│       ├── get_book_case.md         # 用例设计文档
│       └── test_book_subscribe.py   # Book 订阅用例（GB-001 ~ GB-010）
│
├── logs/                            # 运行日志（自动生成）
└── reports/                         # Allure 报告（自动生成）
    └── allure-results/
```

## 环境准备

```bash
cd homework
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 运行用例

```bash
# 运行全部用例
pytest

# 仅 REST 接口
pytest -m rest

# 仅 WebSocket 接口
pytest -m websocket

# 指定用例文件
pytest test_cases/market_data_cases/test_get_candlestick.py -v
pytest test_cases/websocket_subscriptions_cases/test_book_subscribe.py -v

# 按优先级执行
pytest -m P0                # 仅 P0（冒烟/核心）
pytest -m "P0 or P1"        # P0 + P1

# 排除异常用例
pytest -m "not abnormal"

# 仅冒烟用例
pytest -m smoke

# 指定环境运行（TEST_ENV 可选值：test / uat / prod）
TEST_ENV=uat pytest -v
TEST_ENV=uat pytest -m P0 -v

# 指定日志级别
LOG_LEVEL=DEBUG pytest -v

# 组合使用
TEST_ENV=uat LOG_LEVEL=DEBUG pytest -m "rest and P0" -v

# 并行执行（需安装 pytest-xdist）
pytest -n 4                     # 4 个进程并发
pytest -n auto                  # 自动检测 CPU 核数
pytest -n 4 --dist=loadfile     # 按文件分发，同文件用例串行（推荐 WebSocket 用例）

# 并行 + 环境 + 报告
TEST_ENV=uat pytest -n 4 -m P0 --alluredir=reports/allure-results
```

## 查看 Allure 报告

```bash
# 方式一：直接启动临时服务查看报告
allure serve reports/allure-results

# 方式二：生成静态 HTML 报告
allure generate reports/allure-results -o reports/allure-report --clean

# 打开已生成的静态报告
allure open reports/allure-report
```

未安装 Allure 时参见：https://docs.qameta.io/allure/

## 核心模块说明

### 接口定义（test_data）

采用 **API 定义与测试数据分离** 的设计：

```
test_data/{rest|websocket}/{模块}/
├── api_setting.py    # 接口定义（uri、method、response_example）
└── api_data.py       # 测试数据（DDT 参数化、响应示例）
```

**使用方式：**

```python
# REST - Reference and Market Data API
from test_data.rest.market_data import API_GET_CANDLESTICK

# WebSocket - Subscriptions
from test_data.websocket.subscriptions import API_BOOK_SUBSCRIBE
```

### 响应校验（RespChecker）

提供丰富的断言方法，支持 JSONPath 取值：

```python
from utils.checker.response_checker import RespChecker

# 值校验
RespChecker.assert_resp_should_be(data, "$.result.interval", "1m")
RespChecker.assert_biz_success(data)
RespChecker.assert_biz_code(data, BizCode.INVALID_REQUEST)

# 结构校验
RespChecker.assert_resp_structure_be(actual, expected)

# 范围/长度校验
RespChecker.assert_resp_all_in_range(data, "$.result.data[*].t", min_val, max_val)
RespChecker.assert_resp_length_lte(data, "$.result.data", 25)

# 列表校验
RespChecker.assert_resp_all_list_value_same(msgs, "$[*].result.data[0].u")
RespChecker.assert_list_field_increasing(msgs, "result.data.0.u")
RespChecker.assert_list_pu_matches_prev_u(msgs)

# 时间校验
RespChecker.assert_msg_time_interval(msgs, expected_ms=500, tolerance_ms=10)
RespChecker.assert_list_time_step(data, "$.result.data", time_field="t", expected_ms=60000)
```

### WebSocket 客户端

```python
# fixture 自动连接
def test_xxx(self, websocket_market_client):
    client = websocket_market_client
    
    # 订阅
    msg = client.subscribe(params, request_id)
    
    # 持续收包（支持条件终止）
    msgs = client.recv_until(stop_when, max_wait_sec=10.0)
    msgs = client.recv_for_seconds(1.5)
    
    # stop_when 支持两种签名
    stop_when = lambda m: m.get("result", {}).get("channel") == "book.update"
    stop_when = lambda m, msgs: len(msgs) >= 3
```

## 配置说明

| 项 | 说明 |
|----|------|
| 环境变量 | `config/settings.py` 读取 `TEST_ENV`、`REST_BASE_URL`、`WS_MARKET_URL`、`WS_USER_URL` 等 |
| 接口定义 | `RestApiDef` / `WsApiDef`（`constants/api_def.py`）定义接口结构，支持 `param_cases` 多维度参数化 |
| 业务码 | `constants/biz_status.py`：`BizCode.SUCCESS`、`BizCode.INVALID_REQUEST` 等，`get_biz_http_status()` 获取对应 HTTP 状态码 |
| 日志 | `core/logger.get_logger(name)`，控制台 + `logs/` 按日文件 |

## 设计要点

| 要求 | 实现方式 |
|------|----------|
| 基础封装 | `RestClient`（request / request_json_success）、`WebSocketClient`（connect / subscribe / recv_until） |
| 用例与数据分离 | `test_data/` 存 API 定义与参数化数据，`test_cases/` 仅写测试逻辑 |
| 按业务模块组织 | `test_data/rest/market_data/`、`test_data/websocket/subscriptions/` 等 |
| 参数化测试 | `api.get_param_cases("维度名")` 配合 `@pytest.mark.parametrize` |
| Allure 报告 | `@allure.title`、`@allure.step`、`@allure.severity` 完整集成 |
| 统一校验 | `RespChecker` 提供 20+ 断言方法，支持 JSONPath、结构比较、范围校验等 |

## Markers 说明

| Marker | 说明 |
|--------|------|
| `@pytest.mark.rest` | REST 接口用例 |
| `@pytest.mark.websocket` | WebSocket 接口用例 |
| `@pytest.mark.P0` | 冒烟/核心用例 |
| `@pytest.mark.P1` | 重要用例 |
| `@pytest.mark.P2` | 一般用例 |
| `@pytest.mark.smoke` | 冒烟测试 |
| `@pytest.mark.abnormal` | 异常/边界用例 |
