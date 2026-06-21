#!/usr/bin/env python3
"""Cast six Wenwang Liuyao lines with an auditable three-coin simulation."""

from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import sys
from datetime import datetime
from itertools import islice
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ALGORITHM = "tianyan-three-coin-v1"
DOMAIN = b"tianyan-three-coin-v1\0"
ENTROPY_BYTES = 32
LINE_NAMES = {6: "老阴", 7: "少阳", 8: "少阴", 9: "老阳"}


def _validate_entropy(entropy: bytes) -> None:
    if not isinstance(entropy, bytes) or len(entropy) != ENTROPY_BYTES:
        raise ValueError("entropy must contain exactly 32 bytes")


def _digest_for_entropy(entropy: bytes) -> bytes:
    _validate_entropy(entropy)
    return hashlib.sha256(DOMAIN + entropy).digest()


def _coin_bits(entropy: bytes) -> list[int]:
    digest = _digest_for_entropy(entropy)
    return [
        (digest[index // 8] >> (7 - index % 8)) & 1
        for index in range(18)
    ]


def line_from_bits(bits: tuple[int, int, int]) -> dict[str, object]:
    """Convert three unbiased bits into one traditional three-coin line."""
    if len(bits) != 3:
        raise ValueError("a line requires exactly three coin bits")
    if any(bit not in {0, 1} for bit in bits):
        raise ValueError("coin bits must be 0 or 1")

    coin_values = [2 + bit for bit in bits]
    line_value = sum(coin_values)
    return {
        "coins": [
            {"side": "背面" if bit else "字面", "value": value}
            for bit, value in zip(bits, coin_values)
        ],
        "sum": line_value,
        "line_value": line_value,
        "line_name": LINE_NAMES[line_value],
        "moving": line_value in {6, 9},
    }


def _zone(timezone_name: str) -> ZoneInfo:
    try:
        return ZoneInfo(timezone_name)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError(f"unknown timezone: {timezone_name}") from exc


def build_cast(
    question: str,
    timezone_name: str,
    *,
    entropy: bytes | None = None,
    moment: datetime | None = None,
    mode: str = "live",
) -> dict[str, object]:
    """Return a complete, auditable three-coin casting record."""
    question = question.strip()
    if not question:
        raise ValueError("question must not be empty")
    if mode not in {"live", "replay"}:
        raise ValueError("mode must be live or replay")

    zone = _zone(timezone_name)
    if mode == "live":
        if entropy is not None:
            raise ValueError("live mode generates its own entropy")
        entropy = secrets.token_bytes(ENTROPY_BYTES)
        if moment is None:
            moment = datetime.now(zone)
    else:
        if entropy is None:
            raise ValueError("replay mode requires disclosed entropy")
        if moment is None:
            raise ValueError("replay mode requires the original cast time")

    _validate_entropy(entropy)
    if moment.tzinfo is None:
        raise ValueError("cast time must be timezone-aware")
    local_moment = moment.astimezone(zone).replace(second=0, microsecond=0)

    bits = _coin_bits(entropy)
    throws = []
    iterator = iter(bits)
    for line_number in range(1, 7):
        line_bits = tuple(islice(iterator, 3))
        throw = line_from_bits(line_bits)
        throw["line"] = line_number
        throws.append(throw)
    line_values = [throw["line_value"] for throw in throws]

    return {
        "method": "three_coin",
        "algorithm": ALGORITHM,
        "mode": mode,
        "question": question,
        "cast_time": local_moment.strftime("%Y-%m-%d %H:%M"),
        "timezone": timezone_name,
        "entropy_hex": entropy.hex(),
        "derived_sha256_hex": _digest_for_entropy(entropy).hex(),
        "bit_order": "sha256_msb_first",
        "coin_values": {"字面": 2, "背面": 3},
        "input_order": "bottom_to_top",
        "throws": throws,
        "line_values": line_values,
        "line_values_text": ",".join(str(value) for value in line_values),
    }


def _parse_replay_time(text: str, timezone_name: str) -> datetime:
    try:
        parsed = datetime.strptime(text, "%Y-%m-%d %H:%M")
    except ValueError as exc:
        raise ValueError("replay time must use YYYY-MM-DD HH:MM format") from exc
    return parsed.replace(tzinfo=_zone(timezone_name))


def _parse_entropy_hex(text: str) -> bytes:
    try:
        entropy = bytes.fromhex(text)
    except ValueError as exc:
        raise ValueError("replay entropy must be hexadecimal") from exc
    _validate_entropy(entropy)
    return entropy


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Cast six traditional three-coin Liuyao lines as JSON."
    )
    parser.add_argument("--question", required=True, help="The finalized question.")
    parser.add_argument(
        "--timezone", required=True, help="IANA timezone, for example Asia/Shanghai."
    )
    parser.add_argument(
        "--replay-entropy",
        help="Previously disclosed 64-character entropy hex for audit replay.",
    )
    parser.add_argument(
        "--replay-time",
        help="Original cast time for replay: YYYY-MM-DD HH:MM.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        replay_requested = args.replay_entropy is not None or args.replay_time is not None
        if replay_requested:
            if args.replay_entropy is None or args.replay_time is None:
                raise ValueError(
                    "replay entropy and replay time must be provided together"
                )
            cast = build_cast(
                args.question,
                args.timezone,
                entropy=_parse_entropy_hex(args.replay_entropy),
                moment=_parse_replay_time(args.replay_time, args.timezone),
                mode="replay",
            )
        else:
            cast = build_cast(args.question, args.timezone)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(cast, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
