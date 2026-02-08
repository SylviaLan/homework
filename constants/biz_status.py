"""
业务状态（biz status）映射表：biz_code -> http_status, code, message
用于响应校验与断言。
"""
# 表结构：biz_code, http_status, code, message
BIZ_STATUS_TABLE = [
    (0, 200, "--", "Success"),
    (201, 500, "NO_POSITION", "No position"),
    (202, 400, "ACCOUNT_IS_SUSPENDED", "Account is suspended"),
    (203, 500, "ACCOUNTS_DO_NOT_MATCH", "Accounts do not match"),
    (204, 400, "DUPLICATE_CLORDID", "Duplicate client order id"),
    (205, 500, "DUPLICATE_ORDERID", "Duplicate order id"),
    (206, 500, "INSTRUMENT_EXPIRED", "Instrument has expired"),
    (207, 400, "NO_MARK_PRICE", "No mark price"),
    (208, 400, "INSTRUMENT_NOT_TRADABLE", "Instrument is not tradable"),
    (209, 400, "INVALID_INSTRUMENT", "Instrument is invalid"),
    (210, 500, "INVALID_ACCOUNT", "Account is invalid"),
    (211, 500, "INVALID_CURRENCY", "Currency is invalid"),
    (212, 500, "INVALID_ORDERID", "Invalid order id"),
    (213, 400, "INVALID_ORDERQTY", "Invalid order quantity"),
    (214, 500, "INVALID_SETTLE_CURRENCY", "Invalid settlement currency"),
    (215, 500, "INVALID_FEE_CURRENCY", "Invalid fee currency"),
    (216, 500, "INVALID_POSITION_QTY", "Invalid position quantity"),
    (217, 500, "INVALID_OPEN_QTY", "Invalid open quantity"),
    (218, 400, "INVALID_ORDTYPE", "Invalid order_type"),
    (219, 500, "INVALID_EXECINST", "Invalid exec_inst"),
    (220, 400, "INVALID_SIDE", "Invalid side"),
    (221, 400, "INVALID_TIF", "Invalid time_in_force"),
    (222, 400, "STALE_MARK_PRICE", "Stale mark price"),
    (223, 400, "NO_CLORDID", "No client order id"),
    (224, 400, "REJ_BY_MATCHING_ENGINE", "Rejected by matching engine"),
    (225, 400, "EXCEED_MAXIMUM_ENTRY_LEVERAGE", "Exceeds maximum entry leverage"),
    (226, 400, "INVALID_LEVERAGE", "Invalid leverage"),
    (227, 400, "INVALID_SLIPPAGE", "Invalid slippage"),
    (228, 400, "INVALID_FLOOR_PRICE", "Invalid floor price"),
    (229, 400, "INVALID_REF_PRICE", "Invalid ref price"),
    (230, 400, "INVALID_TRIGGER_TYPE", "Invalid ref price type"),
    (301, 500, "ACCOUNT_IS_IN_MARGIN_CALL", "Account is in margin call"),
    (302, 500, "EXCEEDS_ACCOUNT_RISK_LIMIT", "Exceeds account risk limit"),
    (303, 500, "EXCEEDS_POSITION_RISK_LIMIT", "Exceeds position risk limit"),
    (304, 500, "ORDER_WILL_LEAD_TO_IMMEDIATE_LIQUIDATION", "Order will lead to immediate liquidation"),
    (305, 500, "ORDER_WILL_TRIGGER_MARGIN_CALL", "Order will trigger margin call"),
    (306, 500, "INSUFFICIENT_AVAILABLE_BALANCE", "Insufficient available balance"),
    (307, 500, "INVALID_ORDSTATUS", "Invalid order status"),
    (308, 400, "INVALID_PRICE", "Invalid price"),
    (309, 500, "MARKET_IS_NOT_OPEN", "Market is not open"),
    (310, 500, "ORDER_PRICE_BEYOND_LIQUIDATION_PRICE", "Order price beyond liquidation price"),
    (311, 500, "POSITION_IS_IN_LIQUIDATION", "Position is in liquidation"),
    (312, 500, "ORDER_PRICE_GREATER_THAN_LIMITUPPRICE", "Order price is greater than the limit up price"),
    (313, 500, "ORDER_PRICE_LESS_THAN_LIMITDOWNPRICE", "Order price is less than the limit down price"),
    (314, 400, "EXCEEDS_MAX_ORDER_SIZE", "Exceeds max order size"),
    (315, 400, "FAR_AWAY_LIMIT_PRICE", "Far away limit price"),
    (316, 500, "NO_ACTIVE_ORDER", "No active order"),
    (317, 500, "POSITION_NO_EXIST", "Position does not exist"),
    (318, 400, "EXCEEDS_MAX_ALLOWED_ORDERS", "Exceeds max allowed orders"),
    (319, 400, "EXCEEDS_MAX_POSITION_SIZE", "Exceeds max position size"),
    (320, 500, "EXCEEDS_INITIAL_MARGIN", "Exceeds initial margin"),
    (321, 500, "EXCEEDS_MAX_AVAILABLE_BALANCE", "Exceeds maximum availble balance"),
    (401, 400, "ACCOUNT_DOES_NOT_EXIST", "Account does not exist"),
    (406, 500, "ACCOUNT_IS_NOT_ACTIVE", "Account is not active"),
    (407, 500, "MARGIN_UNIT_DOES_NOT_EXIST", "Margin unit does not exist"),
    (408, 400, "MARGIN_UNIT_IS_SUSPENDED", "Margin unit is suspended"),
    (409, 500, "INVALID_USER", "Invalid user"),
    (410, 500, "USER_IS_NOT_ACTIVE", "User is not active"),
    (411, 500, "USER_NO_DERIV_ACCESS", "User does not have derivative access"),
    (412, 500, "ACCOUNT_NO_DERIV_ACCESS", "Account does not have derivative access"),
    (415, 500, "BELOW_MIN_ORDER_SIZE", "Below Min. Order Size"),
    (501, 500, "EXCEED_MAXIMUM_EFFECTIVE_LEVERAGE", "Exceeds maximum effective leverage"),
    (604, 500, "INVALID_COLLATERAL_PRICE", "Invalid collateral price"),
    (605, 500, "INVALID_MARGIN_CALC", "Invalid margin calculation"),
    (606, 500, "EXCEED_ALLOWED_SLIPPAGE", "Exceed allowed slippage"),
    (613, 500, "INVALID_ISOLATION_ID", "Invalid isolation ID"),
    (614, 500, "EXCEEDS_ISOLATED_POSITION_LIMIT", "Exceeds maximum allowed number of isolated position"),
    (615, 500, "ACCOUNT_DOES_NOT_SUPPORT_ISOLATED_POSITION", "Account does not support isolated position"),
    (616, 500, "CREATE_ISOLATED_POSITION_FAILED", "Failed to create isolated position"),
    (617, 500, "DUPLICATED_INSTRUMENT_ORDER_FOR_ISOLATED_MARGIN", "Account already have isolated position with same instrument"),
    (618, 500, "TOO_MANY_PENDING_ISOLATED_MARGIN_REQUESTS", "Exceeds request limit for isoalted margin order"),
    (619, 500, "UNSUPPORTED_OPERATION_ON_ISOLATED_POSITION", "Unsupported operation on isolated position"),
    (620, 500, "CREATE_ISOLATED_POSITION_TIMEOUT", "Request for create isolated position has timed out"),
    (30024, 400, "MAX_AMOUNT_VIOLATED", "If create-withdrawal call quantity > max_withdrawal_balance in user-balance api"),
    (40001, 400, "BAD_REQUEST", "Bad request"),
    (40002, 400, "METHOD_NOT_FOUND", "Method not found"),
    (40003, 400, "INVALID_REQUEST", "Invalid request"),
    (40004, 400, "MISSING_OR_INVALID_ARGUMENT", "Required argument is blank or missing"),
    (40005, 400, "INVALID_DATE", "Invalid date"),
    (40006, 400, "DUPLICATE_REQUEST", "Duplicate request received"),
    (40101, 401, "UNAUTHORIZED", "Not authenticated, or key/signature incorrect"),
    (40102, 400, "INVALID_NONCE", "Nonce value differs by more than 60 seconds"),
    (40103, 401, "IP_ILLEGAL", "IP address not whitelisted"),
    (40104, 401, "USER_TIER_INVALID", "Disallowed based on user tier"),
    (40107, 400, "EXCEED_MAX_SUBSCRIPTIONS", "Session subscription limit has been exceeded"),
    (40401, 200, "NOT_FOUND", "Not found"),
    (40801, 408, "REQUEST_TIMEOUT", "Request has timed out"),
    (42901, 429, "TOO_MANY_REQUESTS", "Requests have exceeded rate limits"),
    (43003, 500, "FILL_OR_KILL", "FOK order has not been filled and cancelled"),
    (43004, 500, "IMMEDIATE_OR_CANCEL", "IOC order has not been filled and cancelled"),
    (43005, 500, "POST_ONLY_REJ", "Rejected POST_ONLY create-order request (normally happened when exec_inst contains POST_ONLY but time_in_force is NOT GOOD_TILL_CANCEL)"),
    (43012, 200, "SELF_TRADE_PREVENTION", "Canceled due to Self Trade Prevention"),
    (50001, 400, "DW_CREDIT_LINE_NOT_MAINTAINED", "If create-withdrawal call breaching credit line check"),
    (50001, 400, "ERR_INTERNAL", "Internal error"),
]

# biz_code -> http_status（同一 biz_code 取表内首次出现的 http_status）
BIZ_CODE_TO_HTTP = {}
for biz_code, http_status, code, message in BIZ_STATUS_TABLE:
    if biz_code not in BIZ_CODE_TO_HTTP:
        BIZ_CODE_TO_HTTP[biz_code] = http_status

# biz_code -> list of {code, message}（支持同一 biz_code 多条）
BIZ_CODE_TO_INFOS = {}
for biz_code, http_status, code, message in BIZ_STATUS_TABLE:
    entry = {"code": code, "message": message, "http_status": http_status}
    if biz_code not in BIZ_CODE_TO_INFOS:
        BIZ_CODE_TO_INFOS[biz_code] = []
    BIZ_CODE_TO_INFOS[biz_code].append(entry)


def get_biz_http_status(biz_code: int) -> int:
    """根据 biz_code 返回期望的 HTTP 状态码，未知返回 500。"""
    return BIZ_CODE_TO_HTTP.get(biz_code, 500)


def get_biz_infos(biz_code: int) -> list:
    """根据 biz_code 返回该码对应的全部 {code, message, http_status} 列表。"""
    return BIZ_CODE_TO_INFOS.get(biz_code, [])


def get_biz_code_str(biz_code: int) -> str:
    """返回首个 code 字符串，用于断言；未知返回 UNKNOWN。"""
    infos = BIZ_CODE_TO_INFOS.get(biz_code)
    return infos[0]["code"] if infos else "UNKNOWN"


# 业务码常量：与 BIZ_STATUS_TABLE 一一对应，显式定义便于 IDE「转到定义」跳转。如 BizCode.INVALID_REQUEST -> 40003。
class BizCode:
    """业务状态码常量。在 IDE 中对 BizCode.INVALID_REQUEST 等使用 Go to Definition 可跳转到本类。"""
    SUCCESS = 0
    NO_POSITION = 201
    ACCOUNT_IS_SUSPENDED = 202
    ACCOUNTS_DO_NOT_MATCH = 203
    DUPLICATE_CLORDID = 204
    DUPLICATE_ORDERID = 205
    INSTRUMENT_EXPIRED = 206
    NO_MARK_PRICE = 207
    INSTRUMENT_NOT_TRADABLE = 208
    INVALID_INSTRUMENT = 209
    INVALID_ACCOUNT = 210
    INVALID_CURRENCY = 211
    INVALID_ORDERID = 212
    INVALID_ORDERQTY = 213
    INVALID_SETTLE_CURRENCY = 214
    INVALID_FEE_CURRENCY = 215
    INVALID_POSITION_QTY = 216
    INVALID_OPEN_QTY = 217
    INVALID_ORDTYPE = 218
    INVALID_EXECINST = 219
    INVALID_SIDE = 220
    INVALID_TIF = 221
    STALE_MARK_PRICE = 222
    NO_CLORDID = 223
    REJ_BY_MATCHING_ENGINE = 224
    EXCEED_MAXIMUM_ENTRY_LEVERAGE = 225
    INVALID_LEVERAGE = 226
    INVALID_SLIPPAGE = 227
    INVALID_FLOOR_PRICE = 228
    INVALID_REF_PRICE = 229
    INVALID_TRIGGER_TYPE = 230
    ACCOUNT_IS_IN_MARGIN_CALL = 301
    EXCEEDS_ACCOUNT_RISK_LIMIT = 302
    EXCEEDS_POSITION_RISK_LIMIT = 303
    ORDER_WILL_LEAD_TO_IMMEDIATE_LIQUIDATION = 304
    ORDER_WILL_TRIGGER_MARGIN_CALL = 305
    INSUFFICIENT_AVAILABLE_BALANCE = 306
    INVALID_ORDSTATUS = 307
    INVALID_PRICE = 308
    MARKET_IS_NOT_OPEN = 309
    ORDER_PRICE_BEYOND_LIQUIDATION_PRICE = 310
    POSITION_IS_IN_LIQUIDATION = 311
    ORDER_PRICE_GREATER_THAN_LIMITUPPRICE = 312
    ORDER_PRICE_LESS_THAN_LIMITDOWNPRICE = 313
    EXCEEDS_MAX_ORDER_SIZE = 314
    FAR_AWAY_LIMIT_PRICE = 315
    NO_ACTIVE_ORDER = 316
    POSITION_NO_EXIST = 317
    EXCEEDS_MAX_ALLOWED_ORDERS = 318
    EXCEEDS_MAX_POSITION_SIZE = 319
    EXCEEDS_INITIAL_MARGIN = 320
    EXCEEDS_MAX_AVAILABLE_BALANCE = 321
    ACCOUNT_DOES_NOT_EXIST = 401
    ACCOUNT_IS_NOT_ACTIVE = 406
    MARGIN_UNIT_DOES_NOT_EXIST = 407
    MARGIN_UNIT_IS_SUSPENDED = 408
    INVALID_USER = 409
    USER_IS_NOT_ACTIVE = 410
    USER_NO_DERIV_ACCESS = 411
    ACCOUNT_NO_DERIV_ACCESS = 412
    BELOW_MIN_ORDER_SIZE = 415
    EXCEED_MAXIMUM_EFFECTIVE_LEVERAGE = 501
    INVALID_COLLATERAL_PRICE = 604
    INVALID_MARGIN_CALC = 605
    EXCEED_ALLOWED_SLIPPAGE = 606
    INVALID_ISOLATION_ID = 613
    EXCEEDS_ISOLATED_POSITION_LIMIT = 614
    ACCOUNT_DOES_NOT_SUPPORT_ISOLATED_POSITION = 615
    CREATE_ISOLATED_POSITION_FAILED = 616
    DUPLICATED_INSTRUMENT_ORDER_FOR_ISOLATED_MARGIN = 617
    TOO_MANY_PENDING_ISOLATED_MARGIN_REQUESTS = 618
    UNSUPPORTED_OPERATION_ON_ISOLATED_POSITION = 619
    CREATE_ISOLATED_POSITION_TIMEOUT = 620
    MAX_AMOUNT_VIOLATED = 30024
    BAD_REQUEST = 40001
    METHOD_NOT_FOUND = 40002
    INVALID_REQUEST = 40003
    MISSING_OR_INVALID_ARGUMENT = 40004
    INVALID_DATE = 40005
    DUPLICATE_REQUEST = 40006
    UNAUTHORIZED = 40101
    INVALID_NONCE = 40102
    IP_ILLEGAL = 40103
    USER_TIER_INVALID = 40104
    EXCEED_MAX_SUBSCRIPTIONS = 40107
    NOT_FOUND = 40401
    REQUEST_TIMEOUT = 40801
    TOO_MANY_REQUESTS = 42901
    FILL_OR_KILL = 43003
    IMMEDIATE_OR_CANCEL = 43004
    POST_ONLY_REJ = 43005
    SELF_TRADE_PREVENTION = 43012
    DW_CREDIT_LINE_NOT_MAINTAINED = 50001
    ERR_INTERNAL = 50001