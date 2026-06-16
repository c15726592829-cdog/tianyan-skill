import json
import subprocess
import sys
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from scripts.pai_gua import (
    build_chart,
    day_ganzhi,
    month_commander,
    parse_cast_time,
    parse_line_values,
    solar_term_utc,
    xunkong_for_index,
)


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "pai_gua.py"


class InputTests(unittest.TestCase):
    def test_accepts_six_line_values_bottom_to_top(self):
        self.assertEqual(parse_line_values("7, 8, 9, 6, 7, 8"), (7, 8, 9, 6, 7, 8))

    def test_accepts_chinese_line_aliases_bottom_to_top(self):
        self.assertEqual(
            parse_line_values("老阴、少阳、少阴、老阳、少阳、少阴"),
            (6, 7, 8, 9, 7, 8),
        )

    def test_rejects_wrong_number_of_lines(self):
        with self.assertRaisesRegex(ValueError, "exactly six"):
            parse_line_values("7,8,9")

    def test_rejects_values_outside_six_to_nine(self):
        with self.assertRaisesRegex(ValueError, "6, 7, 8, or 9"):
            parse_line_values("7,8,5,6,7,8")

    def test_rejects_date_only_cast_time(self):
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD HH:MM"):
            parse_cast_time("2026-06-16", "Asia/Shanghai")

    def test_rejects_hour_only_cast_time(self):
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD HH:MM"):
            parse_cast_time("2026-06-16 15", "Asia/Shanghai")

    def test_rejects_cast_time_with_seconds(self):
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD HH:MM"):
            parse_cast_time("2026-06-16 15:30:00", "Asia/Shanghai")

    def test_accepts_slash_date_and_t_separator_cast_time(self):
        moment = parse_cast_time("2026/06/16T15:30", "Asia/Shanghai")
        self.assertEqual(moment.isoformat(), "2026-06-16T15:30:00+08:00")

    def test_accepts_trailing_timezone_after_strict_time(self):
        moment = parse_cast_time("2026-06-16 15:30 Asia/Shanghai", None)
        self.assertEqual(moment.isoformat(), "2026-06-16T15:30:00+08:00")


class ChartTests(unittest.TestCase):
    def test_pure_qian_chart(self):
        chart = build_chart(
            question="测试",
            cast_time="2024-02-10 12:00",
            timezone_name="Asia/Shanghai",
            line_values="7,7,7,7,7,7",
        )

        self.assertEqual(chart["primary"]["name"], "乾为天")
        self.assertEqual(chart["changed"]["name"], "乾为天")
        self.assertEqual(chart["palace"]["name"], "乾")
        self.assertEqual(chart["palace"]["element"], "金")
        self.assertEqual(chart["palace"]["generation"], "本宫")
        self.assertEqual(chart["shi_line"], 6)
        self.assertEqual(chart["ying_line"], 3)
        self.assertEqual(
            [line["najia"] for line in chart["lines"]],
            ["甲子", "甲寅", "甲辰", "壬午", "壬申", "壬戌"],
        )
        self.assertEqual(
            [line["relative"] for line in chart["lines"]],
            ["子孙", "妻财", "父母", "官鬼", "兄弟", "父母"],
        )
        self.assertEqual(
            [line["spirit"] for line in chart["lines"]],
            ["青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武"],
        )

    def test_pure_kun_chart(self):
        chart = build_chart(
            question="测试",
            cast_time="2024-02-10 12:00",
            timezone_name="Asia/Shanghai",
            line_values="8,8,8,8,8,8",
        )

        self.assertEqual(chart["primary"]["name"], "坤为地")
        self.assertEqual(chart["palace"]["name"], "坤")
        self.assertEqual(chart["palace"]["element"], "土")
        self.assertEqual(
            [line["najia"] for line in chart["lines"]],
            ["乙未", "乙巳", "乙卯", "癸丑", "癸亥", "癸酉"],
        )
        self.assertEqual(
            [line["relative"] for line in chart["lines"]],
            ["兄弟", "父母", "官鬼", "兄弟", "妻财", "子孙"],
        )

    def test_old_yang_changes_to_yin(self):
        chart = build_chart(
            question="测试",
            cast_time="2024-02-10 12:00",
            timezone_name="Asia/Shanghai",
            line_values="9,7,7,7,7,7",
        )

        self.assertEqual(chart["primary"]["name"], "乾为天")
        self.assertEqual(chart["changed"]["name"], "天风姤")
        self.assertEqual(chart["moving_lines"], [1])
        self.assertEqual(chart["lines"][0]["changed_najia"], "辛丑")
        self.assertEqual(chart["lines"][0]["changed_relative"], "父母")

    def test_old_yin_changes_to_yang(self):
        chart = build_chart(
            question="测试",
            cast_time="2024-02-10 12:00",
            timezone_name="Asia/Shanghai",
            line_values="6,8,8,8,8,8",
        )

        self.assertEqual(chart["primary"]["name"], "坤为地")
        self.assertEqual(chart["changed"]["name"], "地雷复")
        self.assertEqual(chart["moving_lines"], [1])

    def test_first_generation_hexagram_has_first_shi(self):
        chart = build_chart(
            question="测试",
            cast_time="2024-02-10 12:00",
            timezone_name="Asia/Shanghai",
            line_values="8,7,7,7,7,7",
        )

        self.assertEqual(chart["primary"]["name"], "天风姤")
        self.assertEqual(chart["palace"]["name"], "乾")
        self.assertEqual(chart["palace"]["generation"], "一世")
        self.assertEqual(chart["shi_line"], 1)
        self.assertEqual(chart["ying_line"], 4)
        self.assertEqual(
            chart["lines"][1]["hidden"],
            {
                "najia": "甲寅",
                "branch_element": "木",
                "relative": "妻财",
            },
        )

    def test_wandering_and_returning_soul_positions(self):
        wandering = build_chart(
            question="测试",
            cast_time="2024-02-10 12:00",
            timezone_name="Asia/Shanghai",
            line_values="8,8,8,7,8,7",
        )
        returning = build_chart(
            question="测试",
            cast_time="2024-02-10 12:00",
            timezone_name="Asia/Shanghai",
            line_values="7,7,7,7,8,7",
        )

        self.assertEqual(wandering["primary"]["name"], "火地晋")
        self.assertEqual(wandering["palace"]["generation"], "游魂")
        self.assertEqual((wandering["shi_line"], wandering["ying_line"]), (4, 1))
        self.assertEqual(returning["primary"]["name"], "火天大有")
        self.assertEqual(returning["palace"]["generation"], "归魂")
        self.assertEqual((returning["shi_line"], returning["ying_line"]), (3, 6))

    def test_all_sixty_four_patterns_are_named_and_assigned(self):
        names = set()
        for mask in range(64):
            values = [7 if mask & (1 << index) else 8 for index in range(6)]
            chart = build_chart(
                question="测试",
                cast_time="2024-02-10 12:00",
                timezone_name="Asia/Shanghai",
                line_values=values,
            )
            names.add(chart["primary"]["name"])
            self.assertIn(chart["palace"]["name"], "乾兑离震巽坎艮坤")
            self.assertIn(chart["shi_line"], range(1, 7))
            self.assertIn(chart["ying_line"], range(1, 7))
        self.assertEqual(len(names), 64)


class CalendarTests(unittest.TestCase):
    def test_known_sexagenary_days(self):
        zone = ZoneInfo("Asia/Shanghai")
        fixtures = [
            (datetime(2000, 1, 7, 12, tzinfo=zone), ("甲子", 0)),
            (datetime(2024, 2, 10, 12, tzinfo=zone), ("甲辰", 40)),
            (datetime(2026, 6, 15, 12, tzinfo=zone), ("庚申", 56)),
        ]
        for moment, expected in fixtures:
            with self.subTest(moment=moment):
                self.assertEqual(day_ganzhi(moment), expected)

    def test_day_changes_at_local_zi_hour(self):
        zone = ZoneInfo("Asia/Shanghai")
        before = datetime(2026, 6, 15, 22, 59, tzinfo=zone)
        after = datetime(2026, 6, 15, 23, 0, tzinfo=zone)
        self.assertEqual(day_ganzhi(before)[0], "庚申")
        self.assertEqual(day_ganzhi(after)[0], "辛酉")

    def test_xunkong_for_each_decade(self):
        self.assertEqual(xunkong_for_index(0), ["戌", "亥"])
        self.assertEqual(xunkong_for_index(10), ["申", "酉"])
        self.assertEqual(xunkong_for_index(20), ["午", "未"])
        self.assertEqual(xunkong_for_index(30), ["辰", "巳"])
        self.assertEqual(xunkong_for_index(40), ["寅", "卯"])
        self.assertEqual(xunkong_for_index(50), ["子", "丑"])

    def test_month_commander_uses_solar_terms(self):
        zone = ZoneInfo("Asia/Shanghai")
        fixtures = [
            (datetime(2024, 1, 20, 12, tzinfo=zone), "丑"),
            (datetime(2024, 2, 10, 12, tzinfo=zone), "寅"),
            (datetime(2024, 3, 10, 12, tzinfo=zone), "卯"),
            (datetime(2024, 4, 10, 12, tzinfo=zone), "辰"),
            (datetime(2024, 5, 10, 12, tzinfo=zone), "巳"),
            (datetime(2024, 6, 10, 12, tzinfo=zone), "午"),
            (datetime(2024, 7, 10, 12, tzinfo=zone), "未"),
            (datetime(2024, 8, 10, 12, tzinfo=zone), "申"),
            (datetime(2024, 9, 10, 12, tzinfo=zone), "酉"),
            (datetime(2024, 10, 10, 12, tzinfo=zone), "戌"),
            (datetime(2024, 11, 10, 12, tzinfo=zone), "亥"),
            (datetime(2024, 12, 10, 12, tzinfo=zone), "子"),
        ]
        for moment, expected in fixtures:
            with self.subTest(moment=moment):
                self.assertEqual(month_commander(moment), expected)

    def test_month_commander_changes_across_solar_term_boundary(self):
        zone = ZoneInfo("Asia/Shanghai")
        boundary = solar_term_utc(2024, "立春").astimezone(zone)
        self.assertEqual(month_commander(boundary - datetime.resolution), "丑")
        self.assertEqual(month_commander(boundary), "寅")

    def test_2024_solar_term_times_are_close_to_almanac(self):
        zone = ZoneInfo("Asia/Shanghai")
        lichun = solar_term_utc(2024, "立春").astimezone(zone)
        jingzhe = solar_term_utc(2024, "惊蛰").astimezone(zone)

        self.assertLess(
            abs((lichun - datetime(2024, 2, 4, 16, 26, tzinfo=zone)).total_seconds()),
            45 * 60,
        )
        self.assertLess(
            abs((jingzhe - datetime(2024, 3, 5, 10, 22, tzinfo=zone)).total_seconds()),
            45 * 60,
        )


class CliTests(unittest.TestCase):
    def test_cli_emits_utf8_json(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--question",
                "测试",
                "--time",
                "2024-02-10 12:00",
                "--timezone",
                "Asia/Shanghai",
                "--lines",
                "7,7,7,7,7,7",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["primary"]["name"], "乾为天")
        self.assertEqual(payload["calendar"]["day"], "甲辰")


if __name__ == "__main__":
    unittest.main()
