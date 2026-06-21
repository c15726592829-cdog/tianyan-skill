import json
import subprocess
import sys
import unittest
from datetime import datetime
from itertools import product
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

from scripts.qi_gua import build_cast, line_from_bits


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "qi_gua.py"
PAI_GUA_SCRIPT = ROOT / "scripts" / "pai_gua.py"
FIXED_ENTROPY = bytes(range(32))
FIXED_ENTROPY_HEX = FIXED_ENTROPY.hex()
FIXED_MOMENT = datetime(
    2026,
    6,
    21,
    15,
    46,
    38,
    tzinfo=ZoneInfo("Asia/Shanghai"),
)


class CoinMappingTests(unittest.TestCase):
    def test_all_coin_combinations_have_traditional_distribution(self):
        values = [
            line_from_bits(bits)["line_value"]
            for bits in product((0, 1), repeat=3)
        ]

        self.assertEqual(
            {value: values.count(value) for value in range(6, 10)},
            {6: 1, 7: 3, 8: 3, 9: 1},
        )

    def test_coin_sides_use_two_for_character_and_three_for_reverse(self):
        line = line_from_bits((0, 1, 0))

        self.assertEqual(
            line["coins"],
            [
                {"side": "字面", "value": 2},
                {"side": "背面", "value": 3},
                {"side": "字面", "value": 2},
            ],
        )
        self.assertEqual(line["line_value"], 7)
        self.assertEqual(line["line_name"], "少阳")
        self.assertFalse(line["moving"])

    def test_rejects_invalid_coin_bits(self):
        with self.assertRaisesRegex(ValueError, "three coin bits"):
            line_from_bits((0, 1))
        with self.assertRaisesRegex(ValueError, "0 or 1"):
            line_from_bits((0, 1, 2))


class CastingTests(unittest.TestCase):
    def test_fixed_entropy_is_reproducible_bottom_to_top(self):
        cast = build_cast(
            "测试",
            "Asia/Shanghai",
            entropy=FIXED_ENTROPY,
            moment=FIXED_MOMENT,
            mode="replay",
        )

        self.assertEqual(cast["method"], "three_coin")
        self.assertEqual(cast["algorithm"], "tianyan-three-coin-v1")
        self.assertEqual(cast["mode"], "replay")
        self.assertEqual(cast["entropy_hex"], FIXED_ENTROPY_HEX)
        self.assertEqual(cast["cast_time"], "2026-06-21 15:46")
        self.assertEqual(cast["timezone"], "Asia/Shanghai")
        self.assertEqual(cast["input_order"], "bottom_to_top")
        self.assertEqual(cast["line_values"], [7, 6, 8, 7, 7, 9])
        self.assertEqual(cast["line_values_text"], "7,6,8,7,7,9")
        self.assertEqual(
            [throw_["line"] for throw_ in cast["throws"]],
            [1, 2, 3, 4, 5, 6],
        )

    def test_live_mode_uses_os_entropy_and_supplied_clock(self):
        with patch("scripts.qi_gua.secrets.token_bytes", return_value=FIXED_ENTROPY):
            cast = build_cast(
                "测试",
                "Asia/Shanghai",
                moment=FIXED_MOMENT,
            )

        self.assertEqual(cast["mode"], "live")
        self.assertEqual(cast["entropy_hex"], FIXED_ENTROPY_HEX)
        self.assertEqual(cast["line_values"], [7, 6, 8, 7, 7, 9])

    def test_replay_requires_exact_entropy_length(self):
        with self.assertRaisesRegex(ValueError, "32 bytes"):
            build_cast(
                "测试",
                "Asia/Shanghai",
                entropy=b"short",
                moment=FIXED_MOMENT,
                mode="replay",
            )

    def test_rejects_unknown_mode(self):
        with self.assertRaisesRegex(ValueError, "live or replay"):
            build_cast(
                "测试",
                "Asia/Shanghai",
                entropy=FIXED_ENTROPY,
                moment=FIXED_MOMENT,
                mode="manual",
            )


class CliTests(unittest.TestCase):
    def test_replay_cli_emits_auditable_utf8_json(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--question",
                "测试",
                "--timezone",
                "Asia/Shanghai",
                "--replay-entropy",
                FIXED_ENTROPY_HEX,
                "--replay-time",
                "2026-06-21 15:46",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["mode"], "replay")
        self.assertEqual(payload["line_values"], [7, 6, 8, 7, 7, 9])
        self.assertEqual(payload["line_values_text"], "7,6,8,7,7,9")
        self.assertEqual(len(payload["throws"]), 6)

    def test_cast_output_can_feed_pai_gua_cli(self):
        cast = build_cast(
            "测试",
            "Asia/Shanghai",
            entropy=FIXED_ENTROPY,
            moment=FIXED_MOMENT,
            mode="replay",
        )

        result = subprocess.run(
            [
                sys.executable,
                str(PAI_GUA_SCRIPT),
                "--question",
                cast["question"],
                "--time",
                cast["cast_time"],
                "--timezone",
                cast["timezone"],
                "--lines",
                cast["line_values_text"],
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        chart = json.loads(result.stdout)
        self.assertEqual(chart["line_values"], cast["line_values"])

    def test_replay_cli_requires_time(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--question",
                "测试",
                "--timezone",
                "Asia/Shanghai",
                "--replay-entropy",
                FIXED_ENTROPY_HEX,
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("replay time", result.stderr)


if __name__ == "__main__":
    unittest.main()
