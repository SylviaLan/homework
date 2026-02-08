# book 订阅（orderbook L2）接口用例

## 业务说明

channel：`book.{instrument_name}.{depth}`，depth 支持 10、50。可选 `book_subscription_type`（SNAPSHOT 默认 / SNAPSHOT_AND_UPDATE）、`book_update_frequency`（10/100 或 500ms）。

**订阅成功后，系统将立即发送一份订单簿快照。** 后续行为取决于订阅类型：

- **快照订阅（SNAPSHOT，默认）**
  - 若订单簿深度发生变化，系统将按请求间隔发布订单簿快照。
  - 即使订单簿无变化，系统仍会**每 500 毫秒强制发布一次快照**。
- **增量订阅（SNAPSHOT_AND_UPDATE）**
  - 若订单簿深度发生变化，系统将按请求间隔通过 **book.update** 推送增量更新。
  - 每次完整的快照/增量更新均包含**逐笔递增的 u 字段**，该字段在同一交易标的中保持唯一性。
  - **仅当更新数据中的 pu 字段与最近接收更新的 u 字段匹配时**，方可处理该更新。
  - 若字段不匹配，则不应应用该更新，此时需**重新订阅以获取全新快照**（直接对该交易标的发起新的订阅请求即可，**无需事先发送退订请求**）。
  - **若持续 5 秒无数据变化，系统将发送空的增量 book.update 心跳信号**：此时买卖盘数据为空（`"asks": [], "bids": []`），仍需按前述规则处理 u 与 pu 字段（订单簿可能在请求深度之外发生更新导致 u 变化）；另可能出于更新序列维护目的发送空增量数据，同样需按规则处理 u/pu。

响应 result 含 instrument_name、subscription、channel、depth、data；data 为 snapshot 时含 asks/bids（level 为 [price, total_size, num_orders]）、tt/t/u；delta 时为 book.update、data 含 update 对象及 u/pu。

---

## 用例列表

| 用例编号 | 所属模块 | 用例名称 | 前置条件 | 用例步骤 | 预期结果 | 优先级 | 备注 |
|--------|----------|----------|----------|----------|----------|--------|------|
| GB-001 | WebSocket/Book | 仅传必填 channels 订阅（默认 SNAPSHOT） | 服务可用、已鉴权 | 1. 连接 market WebSocket<br>2. subscribe，params.channels=["book.BTCUSD-PERP.10"]，不传 book_subscription_type/book_update_frequency | code=0；**立即收到一份订单簿快照**；result 含 instrument_name、subscription、channel、depth、data；data 含 asks/bids；level 为 [price, size, count] 三元组；**无变化时约每 500ms 会再收到快照** | P0 | 默认 SNAPSHOT |
| GB-002 | WebSocket/Book | 指定 depth=10 订阅 | 服务可用、已鉴权 | 1. 连接 market WebSocket<br>2. subscribe，params.channels=["book.BTCUSD-PERP.10"] | code=0；result.depth 为 10；result.subscription 为 book.BTCUSD-PERP.10；**首条为快照**，data 含 asks/bids | P0 | depth 合法值 10、50 |
| GB-003 | WebSocket/Book | 指定 depth=50 订阅 | 服务可用、已鉴权 | 1. 连接 market WebSocket<br>2. subscribe，params.channels=["book.BTCUSD-PERP.50"] | code=0；result.depth 为 50；**首条为快照**；data 含 asks/bids，档位 ≤ 50 | P1 | |
| GB-004 | WebSocket/Book | SNAPSHOT_AND_UPDATE + book_update_frequency=10（增量） | 服务可用、已鉴权 | 1. 连接 market WebSocket<br>2. subscribe，book_subscription_type=SNAPSHOT_AND_UPDATE，book_update_frequency=10<br>3. 持续收包一段时间 | code=0；**首条为 book 快照**（必须含 u）；后续 **book.update** 在深度变化时按 10ms 间隔推送；每条快照/增量均有 u 且 u 同标的中递增；**pu 与上一条 u 一致方可处理**，；**5s 无变化或序列维护可发空心跳**（asks=[], bids=[]），仍含 u/pu 并按上述规则处理 | P1 | 先快照后 delta，10ms 间隔 |
| GB-005 | WebSocket/Book | SNAPSHOT_AND_UPDATE + book_update_frequency=100 | 服务可用、已鉴权 | 1. 连接 market WebSocket<br>2. subscribe，book_subscription_type=SNAPSHOT_AND_UPDATE，book_update_frequency=100 | code=0；首条为 book 快照（含 u）；后续 book.update 按 100ms 间隔；每条含 u，pu 与上一条 u 一致；空心跳同上 | P2 | delta 100ms |
| GB-006 | WebSocket/Book | 不同合约 instrument_name 订阅 | 服务可用、已鉴权 | 1. 连接 market WebSocket<br>2. subscribe，params.channels=["book.ETHUSD-PERP.10"] | code=0；result.instrument_name 为 ETHUSD-PERP；**首条为快照**；data 含 asks/bids | P2 | 可扩展其它合约 |
| GB-007 | WebSocket/Book | 响应结构：result、data、level、u/pu | 服务可用、已鉴权 | 1. 连接 market WebSocket<br>2. subscribe，params.channels=["book.BTCUSD-PERP.10"]<br>3. 校验首条及后续消息 | code=0；result 含 instrument_name、subscription、channel、depth、data；data 项含 asks、bids（快照）或 update（增量）；level 为长度 3 的数组；**快照/更新均含 u**；**增量中 pu 与上一条 u 匹配方可应用**；空心跳时 asks/bids 为空仍含 u/pu | P1 | 与文档 Response Fields 一致 |
| GB-008 | WebSocket/Book | 重新订阅（无需退订） | 已订阅某标的 book | 1. 对同一或另一标的再次 subscribe（不先 unsubscribe） | code=0；**直接收到新快照**，无需先退订 | P2 | 序列不匹配时可重新订阅获取新快照 |
| GB-009 | WebSocket/Book | 缺 channels 或 channels 为空（异常） | 服务可用、已鉴权 | 1. 连接 market WebSocket<br>2. subscribe，params 不包含 channels 或 channels=[] | code 非 0 或连接/订阅失败；返回错误提示 | P2 | 异常/边界 |
| GB-010 | WebSocket/Book | 非法 channel 格式（异常） | 服务可用、已鉴权 | 1. 连接 market WebSocket<br>2. subscribe，params.channels=["invalid.channel"] | code 非 0 或错误提示 | P2 | 异常/边界 |
