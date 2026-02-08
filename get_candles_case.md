# public/get-candlestick 接口用例

| 用例编号 | 所属模块 | 用例名称 | 前置条件 | 用例步骤 | 预期结果 | 优先级 | 创建人 | 备注 |
|----------|----------|----------|----------|----------|----------|--------|--------|------|
| GC-001 | 行情/K线 | 仅传必填参数 instrument_name 获取 K 线 | 服务可用 | 1. GET /public/get-candlestick<br>2. 查询参数：instrument_name=BTCUSD-PERP | HTTP 200；code=0；result 含 interval、data、instrument_name；result.data 至少一条且为数组，每项含 o(open)、h(high)、l(low)、c(close)、v(volume)、t(start time) | P0 | | 默认 timeframe 为 M1，count 默认 25；含结构契约校验 |
| GC-002 | 行情/K线 | 指定 timeframe 为 M1 获取 1 分钟 K 线 | 服务可用 | 1. GET /public/get-candlestick<br>2. 查询参数：instrument_name=BTCUSD-PERP, timeframe=M1 | HTTP 200；code=0；result.interval 为 M1；data 为 K 线数组 | P0 | | Legacy 格式 M1 |
| GC-003 | 行情/K线 | 指定 timeframe 为 M5 获取 5 分钟 K 线 | 服务可用 | 1. GET /public/get-candlestick<br>2. 查询参数：instrument_name=BTCUSD-PERP, timeframe=M5 | HTTP 200；code=0；result.interval 为 M5；data 为 K 线数组 | P0 | | |
| GC-004 | 行情/K线 | 指定 timeframe 为 H1 获取 1 小时 K 线 | 服务可用 | 1. GET /public/get-candlestick<br>2. 查询参数：instrument_name=BTCUSD-PERP, timeframe=H1 | HTTP 200；code=0；result.interval 为 H1；data 为 K 线数组 | P1 | | |
| GC-005 | 行情/K线 | 指定 timeframe 为 1D 获取日 K 线 | 服务可用 | 1. GET /public/get-candlestick<br>2. 查询参数：instrument_name=BTCUSD-PERP, timeframe=1D | HTTP 200；code=0；result.interval 为 1D 或 D1；data 为 K 线数组 | P1 | | 支持 1D/D1/1d |
| GC-006 | 行情/K线 | 指定 count 条数获取 K 线 | 服务可用 | 1. GET /public/get-candlestick<br>2. 查询参数：instrument_name=BTCUSD-PERP, count=10 | HTTP 200；code=0；result.data 长度 ≤ 10 | P1 | | count 默认 25 |
| GC-007 | 行情/K线 | 指定 start_ts 与 end_ts 获取时间区间 K 线 | 服务可用 | 1. GET /public/get-candlestick<br>2. 查询参数：instrument_name=BTCUSD-PERP, start_ts=1613544000000, end_ts=1613630400000 | HTTP 200；code=0；result.data 中每项 t 在 [start_ts, end_ts] 范围内 | P1 | | Unix 毫秒时间戳 |
| GC-008 | 行情/K线 | 全参数：instrument_name + timeframe + count + start_ts + end_ts | 服务可用 | 1. GET /public/get-candlestick<br>2. 查询参数：instrument_name=BTCUSD-PERP, timeframe=M15, count=20, start_ts=1613544000000, end_ts=1613630400000 | HTTP 200；code=0；result.interval=M15；data 长度 ≤ 20 且 t 在指定区间内 | P1 | | |
| GC-009 | 行情/K线 | 不同合约 instrument_name 获取 K 线 | 服务可用 | 1. GET /public/get-candlestick<br>2. 查询参数：instrument_name=ETHUSD-PERP（或其它有效合约） | HTTP 200；code=0；result.instrument_name 与请求一致；data 为 K 线数组 | P2 | | 可扩展其它合约 |
| GC-010 | 行情/K线 | 缺少必填参数 instrument_name | 服务可用 | 1. GET /public/get-candlestick<br>2. 不传或传空 instrument_name | HTTP 4xx 或业务 code 非 0；返回参数错误类提示（如 MISSING_OR_INVALID_ARGUMENT） | P0 | | 必填校验 |
| GC-011 | 行情/K线 | instrument_name 为空字符串 | 服务可用 | 1. GET /public/get-candlestick<br>2. 查询参数：instrument_name= | HTTP 4xx 或 code 非 0；返回参数无效或必填提示 | P1 | | |
| GC-012 | 行情/K线 | instrument_name 为非法/不存在的合约 | 服务可用 | 1. GET /public/get-candlestick<br>2. 查询参数：instrument_name=INVALID-SYMBOL | HTTP 200 或 4xx；code 非 0；返回如 INVALID_INSTRUMENT 等业务错误 | P1 | | |
| GC-013 | 行情/K线 | timeframe 为非法值 | 服务可用 | 1. GET /public/get-candlestick<br>2. 查询参数：instrument_name=BTCUSD-PERP, timeframe=INVALID | HTTP 200 或 4xx；code 非 0 或返回默认/错误提示 | P2 | | 合法值：M1/M5/M15/M30/H1/H2/H4/H12/1D/7D/14D/1M 等 |
| GC-015 | 行情/K线 | start_ts 大于 end_ts 时间区间无效 | 服务可用 | 1. GET /public/get-candlestick<br>2. 查询参数：instrument_name=BTCUSD-PERP, start_ts=1613630400000, end_ts=1613544000000 | HTTP 200 且 code=0 时 data 为空或按实现返回；或返回参数错误 | P2 | | 视接口实现 |
| GC-016 | 行情/K线 | timeframe 为不合法值（空字符串） | 服务可用 | 1. GET /public/get-candlestick<br>2. 查询参数：instrument_name=BTCUSD-PERP, timeframe= | HTTP 200 或 4xx；code 非 0；返回参数错误或非法 timeframe 提示 | P2 | | 不合法值补充用例 |
