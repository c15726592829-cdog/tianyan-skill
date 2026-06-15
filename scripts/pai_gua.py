#!/usr/bin/env python3
"""Build a traditional Wenwang Liuyao Najia chart from six line values."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import datetime, timedelta, timezone
from typing import Iterable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"

TRIGRAM_BY_BITS = {
    (1, 1, 1): "乾",
    (1, 1, 0): "兑",
    (1, 0, 1): "离",
    (1, 0, 0): "震",
    (0, 1, 1): "巽",
    (0, 1, 0): "坎",
    (0, 0, 1): "艮",
    (0, 0, 0): "坤",
}
TRIGRAM_BITS_BY_NAME = {name: bits for bits, name in TRIGRAM_BY_BITS.items()}

TRIGRAM_ELEMENT = {
    "乾": "金",
    "兑": "金",
    "离": "火",
    "震": "木",
    "巽": "木",
    "坎": "水",
    "艮": "土",
    "坤": "土",
}

# Rows are upper trigrams; columns are lower trigrams.
HEXAGRAM_ROWS = {
    "乾": {
        "乾": "乾为天",
        "兑": "天泽履",
        "离": "天火同人",
        "震": "天雷无妄",
        "巽": "天风姤",
        "坎": "天水讼",
        "艮": "天山遁",
        "坤": "天地否",
    },
    "兑": {
        "乾": "泽天夬",
        "兑": "兑为泽",
        "离": "泽火革",
        "震": "泽雷随",
        "巽": "泽风大过",
        "坎": "泽水困",
        "艮": "泽山咸",
        "坤": "泽地萃",
    },
    "离": {
        "乾": "火天大有",
        "兑": "火泽睽",
        "离": "离为火",
        "震": "火雷噬嗑",
        "巽": "火风鼎",
        "坎": "火水未济",
        "艮": "火山旅",
        "坤": "火地晋",
    },
    "震": {
        "乾": "雷天大壮",
        "兑": "雷泽归妹",
        "离": "雷火丰",
        "震": "震为雷",
        "巽": "雷风恒",
        "坎": "雷水解",
        "艮": "雷山小过",
        "坤": "雷地豫",
    },
    "巽": {
        "乾": "风天小畜",
        "兑": "风泽中孚",
        "离": "风火家人",
        "震": "风雷益",
        "巽": "巽为风",
        "坎": "风水涣",
        "艮": "风山渐",
        "坤": "风地观",
    },
    "坎": {
        "乾": "水天需",
        "兑": "水泽节",
        "离": "水火既济",
        "震": "水雷屯",
        "巽": "水风井",
        "坎": "坎为水",
        "艮": "水山蹇",
        "坤": "水地比",
    },
    "艮": {
        "乾": "山天大畜",
        "兑": "山泽损",
        "离": "山火贲",
        "震": "山雷颐",
        "巽": "山风蛊",
        "坎": "山水蒙",
        "艮": "艮为山",
        "坤": "山地剥",
    },
    "坤": {
        "乾": "地天泰",
        "兑": "地泽临",
        "离": "地火明夷",
        "震": "地雷复",
        "巽": "地风升",
        "坎": "地水师",
        "艮": "地山谦",
        "坤": "坤为地",
    },
}

PALACE_SEQUENCES = {
    "乾": ["乾为天", "天风姤", "天山遁", "天地否", "风地观", "山地剥", "火地晋", "火天大有"],
    "坎": ["坎为水", "水泽节", "水雷屯", "水火既济", "泽火革", "雷火丰", "地火明夷", "地水师"],
    "艮": ["艮为山", "山火贲", "山天大畜", "山泽损", "火泽睽", "天泽履", "风泽中孚", "风山渐"],
    "震": ["震为雷", "雷地豫", "雷水解", "雷风恒", "地风升", "水风井", "泽风大过", "泽雷随"],
    "巽": ["巽为风", "风天小畜", "风火家人", "风雷益", "天雷无妄", "火雷噬嗑", "山雷颐", "山风蛊"],
    "离": ["离为火", "火山旅", "火风鼎", "火水未济", "山水蒙", "风水涣", "天水讼", "天火同人"],
    "坤": ["坤为地", "地雷复", "地泽临", "地天泰", "雷天大壮", "泽天夬", "水天需", "水地比"],
    "兑": ["兑为泽", "泽水困", "泽地萃", "泽山咸", "水山蹇", "地山谦", "雷山小过", "雷泽归妹"],
}

GENERATION_NAMES = ["本宫", "一世", "二世", "三世", "四世", "五世", "游魂", "归魂"]
SHI_POSITIONS = [6, 1, 2, 3, 4, 5, 4, 3]

PALACE_LOOKUP = {}
for palace_name, sequence in PALACE_SEQUENCES.items():
    for index, hexagram_name in enumerate(sequence):
        shi = SHI_POSITIONS[index]
        PALACE_LOOKUP[hexagram_name] = {
            "name": palace_name,
            "element": TRIGRAM_ELEMENT[palace_name],
            "generation": GENERATION_NAMES[index],
            "shi": shi,
            "ying": ((shi + 2) % 6) + 1,
        }

NAJIA = {
    "乾": {
        "inner": ["甲子", "甲寅", "甲辰"],
        "outer": ["壬午", "壬申", "壬戌"],
    },
    "坤": {
        "inner": ["乙未", "乙巳", "乙卯"],
        "outer": ["癸丑", "癸亥", "癸酉"],
    },
    "震": {
        "inner": ["庚子", "庚寅", "庚辰"],
        "outer": ["庚午", "庚申", "庚戌"],
    },
    "巽": {
        "inner": ["辛丑", "辛亥", "辛酉"],
        "outer": ["辛未", "辛巳", "辛卯"],
    },
    "坎": {
        "inner": ["戊寅", "戊辰", "戊午"],
        "outer": ["戊申", "戊戌", "戊子"],
    },
    "离": {
        "inner": ["己卯", "己丑", "己亥"],
        "outer": ["己酉", "己未", "己巳"],
    },
    "艮": {
        "inner": ["丙辰", "丙午", "丙申"],
        "outer": ["丙戌", "丙子", "丙寅"],
    },
    "兑": {
        "inner": ["丁巳", "丁卯", "丁丑"],
        "outer": ["丁亥", "丁酉", "丁未"],
    },
}

BRANCH_ELEMENT = {
    "子": "水",
    "亥": "水",
    "寅": "木",
    "卯": "木",
    "巳": "火",
    "午": "火",
    "申": "金",
    "酉": "金",
    "辰": "土",
    "戌": "土",
    "丑": "土",
    "未": "土",
}

GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

SPIRIT_START = {
    "甲": 0,
    "乙": 0,
    "丙": 1,
    "丁": 1,
    "戊": 2,
    "己": 3,
    "庚": 4,
    "辛": 4,
    "壬": 5,
    "癸": 5,
}
SPIRITS = ["青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武"]

SOLAR_TERM_LONGITUDE = {
    "小寒": 285,
    "大寒": 300,
    "立春": 315,
    "雨水": 330,
    "惊蛰": 345,
    "春分": 0,
    "清明": 15,
    "谷雨": 30,
    "立夏": 45,
    "小满": 60,
    "芒种": 75,
    "夏至": 90,
    "小暑": 105,
    "大暑": 120,
    "立秋": 135,
    "处暑": 150,
    "白露": 165,
    "秋分": 180,
    "寒露": 195,
    "霜降": 210,
    "立冬": 225,
    "小雪": 240,
    "大雪": 255,
    "冬至": 270,
}

SOLAR_TERM_APPROXIMATE_DATE = {
    "小寒": (1, 5),
    "大寒": (1, 20),
    "立春": (2, 4),
    "雨水": (2, 19),
    "惊蛰": (3, 5),
    "春分": (3, 20),
    "清明": (4, 4),
    "谷雨": (4, 20),
    "立夏": (5, 5),
    "小满": (5, 21),
    "芒种": (6, 5),
    "夏至": (6, 21),
    "小暑": (7, 6),
    "大暑": (7, 22),
    "立秋": (8, 7),
    "处暑": (8, 23),
    "白露": (9, 7),
    "秋分": (9, 23),
    "寒露": (10, 8),
    "霜降": (10, 23),
    "立冬": (11, 7),
    "小雪": (11, 22),
    "大雪": (12, 7),
    "冬至": (12, 21),
}

MONTH_BOUNDARIES = {
    "小寒": "丑",
    "立春": "寅",
    "惊蛰": "卯",
    "清明": "辰",
    "立夏": "巳",
    "芒种": "午",
    "小暑": "未",
    "立秋": "申",
    "白露": "酉",
    "寒露": "戌",
    "立冬": "亥",
    "大雪": "子",
}


def parse_line_values(values: str | Iterable[int]) -> tuple[int, ...]:
    """Parse six 6/7/8/9 values ordered from the first line upward."""
    if isinstance(values, str):
        tokens = [token for token in re.split(r"[\s,，、/]+", values.strip()) if token]
        try:
            parsed = tuple(int(token) for token in tokens)
        except ValueError as exc:
            raise ValueError("line values must be integers: 6, 7, 8, or 9") from exc
    else:
        parsed = tuple(int(value) for value in values)

    if len(parsed) != 6:
        raise ValueError("line values must contain exactly six entries, bottom to top")
    if any(value not in {6, 7, 8, 9} for value in parsed):
        raise ValueError("each line value must be 6, 7, 8, or 9")
    return parsed


def _line_bits(values: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    primary = tuple(1 if value in {7, 9} else 0 for value in values)
    changed = tuple(
        1 if value == 6 else 0 if value == 9 else primary[index]
        for index, value in enumerate(values)
    )
    return primary, changed


def _hexagram(bits: tuple[int, ...]) -> dict[str, object]:
    lower = TRIGRAM_BY_BITS[bits[:3]]
    upper = TRIGRAM_BY_BITS[bits[3:]]
    return {
        "name": HEXAGRAM_ROWS[upper][lower],
        "lower_trigram": lower,
        "upper_trigram": upper,
        "bits_bottom_to_top": list(bits),
    }


def _najia(bits: tuple[int, ...]) -> list[str]:
    lower = TRIGRAM_BY_BITS[bits[:3]]
    upper = TRIGRAM_BY_BITS[bits[3:]]
    return NAJIA[lower]["inner"] + NAJIA[upper]["outer"]


def _relative(palace_element: str, branch_element: str) -> str:
    if palace_element == branch_element:
        return "兄弟"
    if GENERATES[palace_element] == branch_element:
        return "子孙"
    if GENERATES[branch_element] == palace_element:
        return "父母"
    if CONTROLS[palace_element] == branch_element:
        return "妻财"
    return "官鬼"


def _spirits(day_stem: str) -> list[str]:
    start = SPIRIT_START[day_stem]
    return [SPIRITS[(start + index) % 6] for index in range(6)]


def parse_cast_time(cast_time: str, timezone_name: str | None) -> datetime:
    """Parse an ISO-like local time and attach or convert to an IANA timezone."""
    text = cast_time.strip()
    trailing_zone = None
    if " " in text:
        possible_zone = text.rsplit(" ", 1)[-1]
        if "/" in possible_zone:
            text, trailing_zone = text.rsplit(" ", 1)
    zone_name = timezone_name or trailing_zone
    if not zone_name:
        raise ValueError("a timezone is required, for example Asia/Shanghai")
    try:
        zone = ZoneInfo(zone_name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"unknown IANA timezone: {zone_name}") from exc

    normalized = text.replace("/", "-")
    try:
        moment = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError("cast time must use YYYY-MM-DD HH:MM format") from exc

    if moment.tzinfo is None:
        return moment.replace(tzinfo=zone)
    return moment.astimezone(zone)


def day_ganzhi(moment: datetime) -> tuple[str, int]:
    """Return the sexagenary day, changing days at local 23:00."""
    if moment.tzinfo is None:
        raise ValueError("day calculation requires a timezone-aware datetime")
    effective_date = moment.date()
    if moment.hour >= 23:
        effective_date += timedelta(days=1)
    julian_day_number = effective_date.toordinal() + 1721425
    index = (julian_day_number + 49) % 60
    return STEMS[index % 10] + BRANCHES[index % 12], index


def xunkong_for_index(day_index: int) -> list[str]:
    """Return the two empty branches for a zero-based sexagenary day index."""
    voids = [
        ("戌", "亥"),
        ("申", "酉"),
        ("午", "未"),
        ("辰", "巳"),
        ("寅", "卯"),
        ("子", "丑"),
    ]
    return list(voids[(day_index % 60) // 10])


def _julian_day(moment: datetime) -> float:
    utc = moment.astimezone(timezone.utc)
    seconds = (
        utc.hour * 3600
        + utc.minute * 60
        + utc.second
        + utc.microsecond / 1_000_000
    )
    return utc.date().toordinal() + 1721424.5 + seconds / 86400


def _sun_apparent_longitude(moment: datetime) -> float:
    """Approximate the apparent geocentric solar longitude in degrees."""
    t = (_julian_day(moment) - 2451545.0) / 36525
    mean_longitude = (280.46646 + t * (36000.76983 + t * 0.0003032)) % 360
    mean_anomaly = math.radians(
        (357.52911 + t * (35999.05029 - 0.0001537 * t)) % 360
    )
    center = (
        math.sin(mean_anomaly) * (1.914602 - t * (0.004817 + 0.000014 * t))
        + math.sin(2 * mean_anomaly) * (0.019993 - 0.000101 * t)
        + math.sin(3 * mean_anomaly) * 0.000289
    )
    true_longitude = mean_longitude + center
    omega = math.radians(125.04 - 1934.136 * t)
    return (true_longitude - 0.00569 - 0.00478 * math.sin(omega)) % 360


def solar_term_utc(year: int, term_name: str) -> datetime:
    """Calculate a solar term time in UTC using apparent solar longitude."""
    if not 1800 <= year <= 2200:
        raise ValueError("solar-term calculation supports years 1800 through 2200")
    if term_name not in SOLAR_TERM_LONGITUDE:
        raise ValueError(f"unknown solar term: {term_name}")

    month, day = SOLAR_TERM_APPROXIMATE_DATE[term_name]
    estimate = datetime(year, month, day, 12, tzinfo=timezone.utc)
    target = SOLAR_TERM_LONGITUDE[term_name]
    for _ in range(8):
        longitude = _sun_apparent_longitude(estimate)
        difference = ((longitude - target + 180) % 360) - 180
        estimate -= timedelta(days=difference / 0.98564736)
    return estimate


def month_commander(moment: datetime) -> str:
    """Return the Liuyao month branch using the twelve principal Jie boundaries."""
    if moment.tzinfo is None:
        raise ValueError("month calculation requires a timezone-aware datetime")
    boundaries = []
    for year in (moment.year - 1, moment.year, moment.year + 1):
        for term_name, branch in MONTH_BOUNDARIES.items():
            boundary = solar_term_utc(year, term_name).astimezone(moment.tzinfo)
            boundaries.append((boundary, branch))
    eligible = [item for item in boundaries if item[0] <= moment]
    if not eligible:
        raise ValueError("unable to determine month commander")
    return max(eligible, key=lambda item: item[0])[1]


def build_chart(
    question: str,
    cast_time: str,
    timezone_name: str,
    line_values: str | Iterable[int],
) -> dict[str, object]:
    """Build and return a complete deterministic Wenwang Liuyao chart."""
    values = parse_line_values(line_values)
    moment = parse_cast_time(cast_time, timezone_name)
    primary_bits, changed_bits = _line_bits(values)
    primary = _hexagram(primary_bits)
    changed = _hexagram(changed_bits)
    palace = PALACE_LOOKUP[primary["name"]]
    primary_najia = _najia(primary_bits)
    changed_najia = _najia(changed_bits)
    day_name, day_index = day_ganzhi(moment)
    spirits = _spirits(day_name[0])
    moving_lines = [index + 1 for index, value in enumerate(values) if value in {6, 9}]
    primary_relatives = [
        _relative(palace["element"], BRANCH_ELEMENT[najia[1]])
        for najia in primary_najia
    ]
    present_relatives = set(primary_relatives)
    palace_bits = TRIGRAM_BITS_BY_NAME[palace["name"]] * 2
    hidden_najia = _najia(palace_bits)
    hidden_relatives = [
        _relative(palace["element"], BRANCH_ELEMENT[najia[1]])
        for najia in hidden_najia
    ]

    lines = []
    for index, value in enumerate(values):
        branch = primary_najia[index][1]
        changed_branch = changed_najia[index][1]
        line_number = index + 1
        hidden = None
        if hidden_relatives[index] not in present_relatives:
            hidden_branch = hidden_najia[index][1]
            hidden = {
                "najia": hidden_najia[index],
                "branch_element": BRANCH_ELEMENT[hidden_branch],
                "relative": hidden_relatives[index],
            }
        lines.append(
            {
                "line": line_number,
                "value": value,
                "yin_yang": "阳" if primary_bits[index] else "阴",
                "moving": value in {6, 9},
                "shi": line_number == palace["shi"],
                "ying": line_number == palace["ying"],
                "najia": primary_najia[index],
                "branch_element": BRANCH_ELEMENT[branch],
                "relative": primary_relatives[index],
                "hidden": hidden,
                "spirit": spirits[index],
                "changed_yin_yang": "阳" if changed_bits[index] else "阴",
                "changed_najia": changed_najia[index],
                "changed_branch_element": BRANCH_ELEMENT[changed_branch],
                "changed_relative": _relative(
                    palace["element"], BRANCH_ELEMENT[changed_branch]
                ),
            }
        )

    return {
        "question": question.strip(),
        "cast_time": moment.isoformat(),
        "timezone": getattr(moment.tzinfo, "key", str(moment.tzinfo)),
        "input_order": "bottom_to_top",
        "line_values": list(values),
        "moving_lines": moving_lines,
        "primary": primary,
        "changed": changed,
        "palace": {
            "name": palace["name"],
            "element": palace["element"],
            "generation": palace["generation"],
        },
        "shi_line": palace["shi"],
        "ying_line": palace["ying"],
        "calendar": {
            "month_commander": month_commander(moment),
            "day": day_name,
            "day_index": day_index,
            "xunkong": xunkong_for_index(day_index),
            "day_boundary": "23:00 local time",
        },
        "lines": lines,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a traditional Wenwang Liuyao Najia chart as JSON."
    )
    parser.add_argument("--question", required=True, help="The divination question.")
    parser.add_argument("--time", required=True, help="Cast time: YYYY-MM-DD HH:MM.")
    parser.add_argument(
        "--timezone", required=True, help="IANA timezone, for example Asia/Shanghai."
    )
    parser.add_argument(
        "--lines",
        required=True,
        help="Six 6/7/8/9 values ordered bottom to top.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        chart = build_chart(args.question, args.time, args.timezone, args.lines)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(chart, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
