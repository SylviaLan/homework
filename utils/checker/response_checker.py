"""
响应校验工具：提供丰富的断言方法，支持 jsonpath 取值、结构比较、范围校验等。
所有 checker 方法以 assert 开头，内含 assert 语句，pytest 会拦截并生成 error trace。
"""
from __future__ import annotations

from typing import Any

import allure
import jsonpath

from core.logger import get_logger

logger = get_logger("response_checker")


class RespChecker:
    """响应校验器：提供各类断言方法，支持 allure step 记录。"""

    # ========== 基础值校验 ==========

    @classmethod
    @allure.step("断言响应值应该为 {expected_value}")
    def assert_resp_should_be(cls, resp: dict, json_path: str, expected_value: Any):
        """
        校验 jsonpath 取值等于期望值。
        Args:
            resp: 响应 dict
            json_path: jsonpath 表达式，如 '$.result.interval'
            expected_value: 期望值
        """
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret, f"jsonpath '{json_path}' 未匹配到任何值"
        actual = ret[0]
        logger.info("assert %s == 期望值 %s", actual, expected_value)
        assert actual == expected_value, f"期望 {expected_value}，实际 {actual}"

    @classmethod
    @allure.step("断言响应值不应该为 {expected_value}")
    def assert_resp_should_not_be(cls, resp: dict, json_path: str, expected_value: Any):
        """校验 jsonpath 取值不等于期望值。"""
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret, f"jsonpath '{json_path}' 未匹配到任何值"
        actual = ret[0]
        assert actual != expected_value, f"期望不等于 {expected_value}，实际 {actual}"

    @classmethod
    @allure.step("断言响应值不为空")
    def assert_resp_not_none(cls, resp: dict, json_path: str):
        """校验 jsonpath 取值不为 None。"""
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret, f"jsonpath '{json_path}' 未匹配到任何值"
        actual = ret[0]
        assert actual is not None, f"'{json_path}' 期望非 None，实际为 None"

    @classmethod
    @allure.step("断言响应值在期望列表中")
    def assert_resp_should_in(cls, resp: dict, json_path: str, expected_values: list | set | tuple):
        """
        校验 jsonpath 取值在期望列表中。
        Args:
            resp: 响应 dict
            json_path: jsonpath 表达式
            expected_values: 期望值列表
        """
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret, f"jsonpath '{json_path}' 未匹配到任何值"
        actual = ret[0]
        assert actual in expected_values, f"期望 {actual} 在 {expected_values} 中"

    # ========== 包含校验 ==========

    @classmethod
    @allure.step("断言响应值包含 {expected_value}")
    def assert_resp_should_contain(cls, resp: dict, json_path: str, expected_value: Any):
        """校验 jsonpath 取值包含期望值（字符串/列表）。"""
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret, f"jsonpath '{json_path}' 未匹配到任何值"
        actual = ret[0]
        assert expected_value in actual, f"期望 '{expected_value}' 在 '{actual}' 中"

    @classmethod
    @allure.step("断言响应值不包含 {expected_value}")
    def assert_resp_not_contain(cls, resp: dict, json_path: str, expected_value: Any):
        """校验 jsonpath 取值不包含期望值。"""
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret, f"jsonpath '{json_path}' 未匹配到任何值"
        actual = ret[0]
        assert expected_value not in actual, f"期望 '{expected_value}' 不在 '{actual}' 中"

    # ========== 长度校验 ==========

    @classmethod
    @allure.step("断言响应列表长度等于 {expected_len}")
    def assert_resp_length_should_be(cls, resp: dict, json_path: str, expected_len: int):
        """校验 jsonpath 取值长度等于期望值。"""
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret, f"jsonpath '{json_path}' 未匹配到任何值"
        actual = ret[0]
        assert len(actual) == expected_len, f"期望长度 {expected_len}，实际 {len(actual)}"

    @classmethod
    @allure.step("断言响应列表长度 >= {min_len}")
    def assert_resp_length_gte(cls, resp: dict, json_path: str, min_len: int):
        """校验 jsonpath 取值长度大于等于 min_len。"""
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret, f"jsonpath '{json_path}' 未匹配到任何值"
        actual = ret[0]
        assert len(actual) >= min_len, f"期望长度 >= {min_len}，实际 {len(actual)}"

    @classmethod
    @allure.step("断言响应列表长度 <= {max_len}")
    def assert_resp_length_lte(cls, resp: dict, json_path: str, max_len: int):
        """校验 jsonpath 取值长度小于等于 max_len。"""
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret, f"jsonpath '{json_path}' 未匹配到任何值"
        actual = ret[0]
        assert len(actual) <= max_len, f"期望长度 <= {max_len}，实际 {len(actual)}"

    @classmethod
    @allure.step("断言响应列表至少一条")
    def assert_resp_should_has_mt_one(cls, resp: dict, json_path: str):
        """校验 jsonpath 取值长度至少为 1。"""
        cls.assert_resp_length_gte(resp, json_path, 1)

    # ========== 范围校验 ==========

    @classmethod
    @allure.step("断言响应值在范围 [{min_val}, {max_val}]")
    def assert_resp_in_range(cls, resp: dict, json_path: str, min_val: Any, max_val: Any):
        """
        校验 jsonpath 取值在 [min_val, max_val] 范围内。
        Args:
            resp: 响应 dict
            json_path: jsonpath 表达式
            min_val: 最小值（含）
            max_val: 最大值（含）
        """
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret, f"jsonpath '{json_path}' 未匹配到任何值"
        actual = ret[0]
        assert min_val <= actual <= max_val, f"期望 {actual} 在 [{min_val}, {max_val}] 范围内"

    @classmethod
    @allure.step("断言列表所有值在范围 [{min_val}, {max_val}]")
    def assert_resp_all_in_range(cls, resp: dict, json_path: str, min_val: Any, max_val: Any):
        """
        校验 jsonpath 取值列表中所有元素都在 [min_val, max_val] 范围内。
        Args:
            resp: 响应 dict
            json_path: jsonpath 表达式，如 '$.result.data[*].t'
            min_val: 最小值（含）
            max_val: 最大值（含）
        """
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret, f"jsonpath '{json_path}' 未匹配到任何值"
        for i, val in enumerate(ret):
            assert min_val <= val <= max_val, f"第 {i} 项 {val} 不在 [{min_val}, {max_val}] 范围内"

    # ========== 列表字段校验 ==========

    @classmethod
    @allure.step("断言响应列表所有项的字段值等于 {expected_value}")
    def assert_resp_all_list_value_should_be(cls, resp: dict, json_path: str, expected_value: Any):
        """
        校验 jsonpath 取值列表中所有元素都等于期望值。
        Example: $.result.data[*].status 全为 1
        """
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret, f"jsonpath '{json_path}' 未匹配到任何值"
        assert all(i == expected_value for i in ret), f"期望所有值为 {expected_value}，实际 {ret}"

    @classmethod
    @allure.step("断言响应列表所有项的字段值彼此一致")
    def assert_resp_all_list_value_same(cls, resp: dict, json_path: str):
        """
        校验 jsonpath 取值列表中所有元素彼此相同（不指定期望值）。
        Example: $.result.data[*].instrument_name 全部相同
        Args:
            resp: 响应 dict
            json_path: jsonpath 表达式，如 '$.result.data[*].instrument_name'
        """
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret, f"jsonpath '{json_path}' 未匹配到任何值"
        if len(ret) <= 1:
            return  # 0 或 1 个元素，无需比较
        first = ret[0]
        for i, val in enumerate(ret[1:], start=1):
            assert val == first, f"第 {i} 项值 {val} 与第 0 项 {first} 不一致"

    @classmethod
    @allure.step("断言响应列表所有项的字段值包含 {expected_value}")
    def assert_resp_all_list_value_should_contain(cls, resp: dict, json_path: str, expected_value: Any):
        """校验 jsonpath 取值列表中所有元素都包含期望值。"""
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret, f"jsonpath '{json_path}' 未匹配到任何值"
        assert all(expected_value in i for i in ret), f"期望所有值包含 {expected_value}，实际 {ret}"

    @classmethod
    @allure.step("断言响应列表中存在值在期望列表中")
    def assert_resp_list_value_should_in(cls, resp: dict, json_path: str, expected_values: list | set | tuple):
        """校验 jsonpath 取值列表中至少有一个元素在期望列表中。"""
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret, f"jsonpath '{json_path}' 未匹配到任何值"
        assert any(i in expected_values for i in ret), f"期望至少一个值在 {expected_values} 中，实际 {ret}"

    @classmethod
    @allure.step("断言响应列表取值应为")
    def assert_resp_list_should_be(cls, resp: dict, json_path: str, expected_value: list):
        """校验 jsonpath 取值列表完全等于期望列表。"""
        ret = jsonpath.jsonpath(resp, json_path)
        assert ret == expected_value, f"期望 {expected_value}，实际 {ret}"

    # ========== HTTP / 业务码校验 ==========

    @classmethod
    @allure.step("断言 HTTP 状态码为 {expected_status}")
    def assert_http_status(cls, resp, expected_status: int):
        """
        校验 HTTP 响应状态码。
        Args:
            resp: requests.Response 对象
            expected_status: 期望的 HTTP 状态码
        """
        actual = resp.status_code
        assert actual == expected_status, f"HTTP 状态码期望 {expected_status}，实际 {actual}"

    @classmethod
    @allure.step("断言业务码为 {expected_code}")
    def assert_biz_code(cls, resp_json: dict, expected_code: int, code_key: str = "code"):
        """
        校验业务响应码。
        Args:
            resp_json: 响应 JSON dict
            expected_code: 期望的业务码
            code_key: 业务码字段名，默认 "code"
        """
        actual = resp_json.get(code_key)
        assert actual == expected_code, f"业务码期望 {expected_code}，实际 {actual}"

    @classmethod
    @allure.step("断言业务成功（code=0）")
    def assert_biz_success(cls, resp_json: dict, code_key: str = "code"):
        """校验业务响应成功（code == 0）。"""
        cls.assert_biz_code(resp_json, 0, code_key)

    # ========== 时间间隔校验 ==========

    @classmethod
    @allure.step("断言消息时间间隔约 {expected_ms}ms")
    def assert_msg_time_interval(
        cls,
        msgs: list[dict],
        expected_ms: int,
        tolerance_ms: int = 5,
        idx0: int = 0,
        idx1: int = 1,
        time_path: str = "result.data.0.t",
    ):
        """
        校验两条消息的时间间隔。
        Args:
            msgs: 消息列表
            expected_ms: 期望的时间间隔（毫秒）
            tolerance_ms: 允许误差（毫秒），默认 5ms
            idx0: 第一条消息的索引，默认 0
            idx1: 第二条消息的索引，默认 1
            time_path: 时间戳字段路径（点分隔），默认 "result.data.0.t"
        Example:
            # 校验第0条和第1条消息间隔约 500ms
            RespChecker.assert_msg_time_interval(follow_msgs, 500)

            # 校验第1条和第2条消息间隔约 5000ms，允许 100ms 误差
            RespChecker.assert_msg_time_interval(follow_msgs, 5000, tolerance_ms=100, idx0=1, idx1=2)
        """
        min_idx = max(idx0, idx1) + 1
        assert len(msgs) >= min_idx, f"需要至少 {min_idx} 条消息来校验时间间隔，实际收到 {len(msgs)} 条"

        def _get_time(msg: dict, path: str) -> int | None:
            """根据点分隔路径获取时间戳"""
            val = msg
            for key in path.split("."):
                if val is None:
                    return None
                if key.isdigit():
                    key = int(key)
                    val = val[key] if isinstance(val, list) and len(val) > key else None
                else:
                    val = val.get(key) if isinstance(val, dict) else None
            return val

        t0 = _get_time(msgs[idx0], time_path)
        t1 = _get_time(msgs[idx1], time_path)
        assert t0 is not None and t1 is not None, f"消息缺少时间戳：msgs[{idx0}].{time_path}={t0}, msgs[{idx1}].{time_path}={t1}"

        diff_ms = t1 - t0
        min_ms = expected_ms - tolerance_ms
        max_ms = expected_ms + tolerance_ms
        assert min_ms <= diff_ms <= max_ms, (
            f"时间间隔应约 {expected_ms}ms（±{tolerance_ms}ms），实际 {diff_ms}ms"
        )

    @classmethod
    @allure.step("断言列表相邻项时间步长")
    def assert_list_time_step(
        cls,
        resp: dict,
        json_path: str,
        time_field: str = "t",
        expected_ms: int = None,
        min_ms: int = None,
        max_ms: int = None,
    ):
        """
        校验列表中所有相邻元素的时间步长。

        Args:
            resp: 响应 dict
            json_path: 列表的 JSONPath，如 "$.result.data"
            time_field: 列表元素中的时间字段名，默认 "t"
            expected_ms: 精确步长（毫秒），与 min_ms/max_ms 二选一
            min_ms: 最小步长（毫秒），用于不固定间隔场景（如月份）
            max_ms: 最大步长（毫秒），与 min_ms 配合使用

        Example:
            # 精确步长：1分钟 K 线，步长 60000ms
            RespChecker.assert_list_time_step(data, "$.result.data", time_field="t", expected_ms=60000)

            # 范围步长：1月 K 线，步长 28~31 天
            RespChecker.assert_list_time_step(data, "$.result.data", time_field="t",
                                              min_ms=28*86400000, max_ms=31*86400000)
        """
        matches = jsonpath.jsonpath(resp, json_path)
        assert matches, f"JSONPath {json_path} 未匹配到数据"
        items = matches if isinstance(matches[0], dict) else matches[0]
        assert isinstance(items, list), f"JSONPath {json_path} 应返回列表，实际类型 {type(items).__name__}"

        if len(items) < 2:
            return  # 不足 2 项无法校验步长

        # 按时间字段排序
        sorted_items = sorted(items, key=lambda x: x.get(time_field, 0))

        for i in range(len(sorted_items) - 1):
            t_cur = sorted_items[i].get(time_field)
            t_next = sorted_items[i + 1].get(time_field)
            assert t_cur is not None and t_next is not None, (
                f"列表项 [{i}] 或 [{i+1}] 缺少时间字段 '{time_field}'"
            )
            diff = t_next - t_cur

            if expected_ms is not None:
                assert diff == expected_ms, (
                    f"相邻项 [{i}]->[{i+1}] 时间步长应为 {expected_ms}ms，实际 {diff}ms"
                )
            elif min_ms is not None and max_ms is not None:
                assert min_ms <= diff <= max_ms, (
                    f"相邻项 [{i}]->[{i+1}] 时间步长应在 {min_ms}~{max_ms}ms，实际 {diff}ms"
                )
            else:
                raise ValueError("需指定 expected_ms 或 min_ms+max_ms")

    @classmethod
    @allure.step("断言列表字段递增")
    def assert_list_field_increasing(
        cls,
        items: list[dict],
        field_path: str = "result.data.0.u",
        strict: bool = False,
    ):
        """
        校验列表中每项指定字段的值递增（或非递减）。

        Args:
            items: 消息列表
            field_path: 字段路径（点分隔），默认 "result.data.0.u"
            strict: 是否严格递增（True: 后一条 > 前一条；False: 后一条 >= 前一条）

        Example:
            # 校验 u 字段非递减
            RespChecker.assert_list_field_increasing(msgs, "result.data.0.u")

            # 校验 u 字段严格递增
            RespChecker.assert_list_field_increasing(msgs, "result.data.0.u", strict=True)
        """
        if len(items) < 2:
            return

        def _get_value(item: dict, path: str):
            val = item
            for key in path.split("."):
                if val is None:
                    return None
                if key.isdigit():
                    key = int(key)
                    val = val[key] if isinstance(val, list) and len(val) > key else None
                else:
                    val = val.get(key) if isinstance(val, dict) else None
            return val

        for i in range(len(items) - 1):
            v_cur = _get_value(items[i], field_path)
            v_next = _get_value(items[i + 1], field_path)
            assert v_cur is not None and v_next is not None, (
                f"列表项 [{i}] 或 [{i+1}] 缺少字段 '{field_path}'：v_cur={v_cur}, v_next={v_next}"
            )
            if strict:
                assert v_next > v_cur, (
                    f"字段 '{field_path}' 应严格递增：[{i}]={v_cur}, [{i+1}]={v_next}"
                )
            else:
                assert v_next >= v_cur, (
                    f"字段 '{field_path}' 应递增（非递减）：[{i}]={v_cur}, [{i+1}]={v_next}"
                )

    @classmethod
    @allure.step("断言列表相邻项 pu == 前一条 u")
    def assert_list_pu_matches_prev_u(
        cls,
        items: list[dict],
        u_path: str = "result.data.0.u",
        pu_path: str = "result.data.0.pu",
    ):
        """
        校验列表中相邻项的 pu 字段等于前一条的 u 字段。

        Args:
            items: 消息列表（需至少 2 条）
            u_path: u 字段路径（点分隔），默认 "result.data.0.u"
            pu_path: pu 字段路径（点分隔），默认 "result.data.0.pu"

        Example:
            # 校验增量订阅消息的 pu == 前一条 u
            RespChecker.assert_list_pu_matches_prev_u(update_msgs)
        """
        if len(items) < 2:
            return

        def _get_value(item: dict, path: str):
            val = item
            for key in path.split("."):
                if val is None:
                    return None
                if key.isdigit():
                    key = int(key)
                    val = val[key] if isinstance(val, list) and len(val) > key else None
                else:
                    val = val.get(key) if isinstance(val, dict) else None
            return val

        for i in range(len(items) - 1):
            u_cur = _get_value(items[i], u_path)
            pu_next = _get_value(items[i + 1], pu_path)
            assert u_cur is not None, f"列表项 [{i}] 缺少字段 '{u_path}'"
            assert pu_next is not None, f"列表项 [{i+1}] 缺少字段 '{pu_path}'"
            assert pu_next == u_cur, (
                f"[{i+1}].pu 应等于 [{i}].u：pu={pu_next}, prev_u={u_cur}"
            )

    @classmethod
    @allure.step('断言响应结构与期望一致')
    def assert_resp_structure_be(
        cls,
        actual: dict,
        expected: dict,
        path: str = "$",
        check_list_item: bool = True,
        allow_extra_keys: bool = True,
    ):
        """
        递归比较两个 dict 的结构是否一致（只比较键名和类型，不比较具体值）。

        Args:
            actual: 实际响应 dict
            expected: 期望结构 dict（可用接口文档示例）
            path: 当前路径（用于错误提示），默认 "$"
            check_list_item: 是否检查列表元素结构（取首项比较），默认 True
            allow_extra_keys: 是否允许实际响应有额外的键（默认 True，兼容 API 新增字段）

        Raises:
            AssertionError: 结构不一致时抛出，包含具体差异路径

        Example:
            expected = {"code": 0, "result": {"data": [{"id": 1, "name": "x"}]}}
            actual = {"code": 0, "result": {"data": [{"id": 123, "name": "test"}]}}
            RespChecker.assert_resp_structure_be(actual, expected)  # 通过

            actual_extra = {"code": 0, "result": {"data": [...], "new_field": 1}}
            RespChecker.assert_resp_structure_be(actual_extra, expected)  # 通过（allow_extra_keys=True）

            actual_bad = {"code": 0, "result": {"items": []}}  # 缺少 data
            RespChecker.assert_resp_structure_be(actual_bad, expected)  # 失败
        """
        diff = cls._compare_structure(actual, expected, path, check_list_item, allow_extra_keys)
        assert not diff, f"结构不一致:\n" + "\n".join(diff)

    @classmethod
    def _compare_structure(
        cls,
        actual,
        expected,
        path: str,
        check_list_item: bool,
        allow_extra_keys: bool,
    ) -> list[str]:
        """
        递归比较结构，返回差异列表。
        """
        diff = []

        # 类型不同
        if type(actual) != type(expected):
            diff.append(f"{path}: 类型不同，期望 {type(expected).__name__}，实际 {type(actual).__name__}")
            return diff

        # dict: 比较键
        if isinstance(expected, dict):
            expected_keys = set(expected.keys())
            actual_keys = set(actual.keys())

            missing = expected_keys - actual_keys
            extra = actual_keys - expected_keys

            if missing:
                diff.append(f"{path}: 缺少键 {missing}")
            if extra and not allow_extra_keys:
                diff.append(f"{path}: 多余键 {extra}")

            # 递归比较共有键
            for key in expected_keys & actual_keys:
                sub_diff = cls._compare_structure(
                    actual[key], expected[key], f"{path}.{key}", check_list_item, allow_extra_keys
                )
                diff.extend(sub_diff)

        # list: 比较首项结构
        elif isinstance(expected, list) and check_list_item:
            if expected and actual:
                sub_diff = cls._compare_structure(
                    actual[0], expected[0], f"{path}[0]", check_list_item, allow_extra_keys
                )
                diff.extend(sub_diff)
            elif expected and not actual:
                diff.append(f"{path}: 期望非空列表，实际为空")

        return diff

    @classmethod
    @allure.step('断言响应结构包含期望键')
    def assert_resp_structure_contains(
        cls,
        actual: dict,
        expected_keys: set[str] | list[str],
        path: str = "$",
    ):
        """
        断言 actual 包含 expected_keys 中的所有键（允许 actual 有额外键）。

        Args:
            actual: 实际响应 dict
            expected_keys: 期望必须存在的键集合
            path: 当前路径（用于错误提示）

        Example:
            actual = {"code": 0, "result": {"id": 1, "name": "x", "extra": "y"}}
            RespChecker.assert_resp_structure_contains(actual["result"], {"id", "name"})  # 通过
        """
        expected_set = set(expected_keys)
        actual_keys = set(actual.keys()) if isinstance(actual, dict) else set()
        missing = expected_set - actual_keys
        assert not missing, f"{path}: 缺少必要键 {missing}，实际键 {actual_keys}"


def get_response_structure_keys(
    response_example: dict | None,
    result_key: str = "result",
    data_key: str = "data",
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """
    从 response_example 提取 result 层键与 data 首项键，用于结构校验。
    :param response_example: 接口响应示例（如 RestApiDef.response_example）
    :param result_key: result 在响应中的键，默认 "result"
    :param data_key: 列表字段在 result 中的键，默认 "data"
    :return: (result_keys, data_item_keys)，如 (("interval", "instrument_name", "data"), ("o", "h", "l", "c", "v", "t"))
    """
    _resp = response_example or {}
    _result = _resp.get(result_key) or {}
    result_keys = tuple(_result.keys())
    _data = _result.get(data_key) or [{}]
    _data_sample = _data[0] if _data else {}
    data_item_keys = tuple(_data_sample.keys())
    return result_keys, data_item_keys
