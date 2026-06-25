from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re
import sys


MODULE_IDS = (
    "people-identity",
    "thoughts-intentions",
    "romance-marriage",
    "contact-actions",
    "location-direction",
    "timing",
    "objects-lost-property",
    "travel-whereabouts",
    "work-career",
    "money-debt",
    "business-partnership",
    "contracts-documents",
    "study-exams",
    "health-medicine",
    "family-relatives",
    "children-pregnancy",
    "housing-property",
    "disputes-litigation",
    "outcomes-development",
    "strategy-comparison",
)

MODULE_HEADINGS = (
    "## Scope",
    "## Trigger Questions",
    "## Exclusions and Redirects",
    "## Question Subject",
    "## Perspective",
    "## Primary Anchor or Useful Spirit",
    "## Secondary References",
    "## Anchor Conflict Resolution",
    "## Month and Day",
    "## Moving and Changed Lines",
    "## Shi and Ying",
    "## Branch Structures, Void, Break, Tomb, and Hidden Spirit",
    "## Hexagram and Trigram Corroboration",
    "## Allowed Answer Resolution",
    "## Required Contrary Evidence",
    "## Prohibited Inferences",
    "## Source Rule IDs",
    "## Worked Structural Examples",
)

SOURCE_FIELDS = (
    "Status",
    "Book",
    "Location",
    "Locator",
    "Original",
    "Operational rule",
    "Conditions",
    "Exceptions",
    "Conflicts",
    "Modern extension",
)

SOURCE_FILENAMES = (
    "zhouyi-shuogua.md",
    "jingshi-yizhuan.md",
    "huozhulin.md",
    "zengshan-buyi.md",
    "bushi-zhengzong.md",
)

SOURCE_ID_PATTERN = re.compile(r"^### ([A-Z]{2,5}-[A-Z0-9-]+-\d{3})$")
FIELD_PATTERN = re.compile(r"^- ([A-Za-z ]+):\s*(.+)$")
SOURCE_REF_PATTERN = re.compile(r"\b[A-Z]{2,5}-[A-Z0-9-]+-\d{3}\b")
INDEX_ROW_PATTERN = re.compile(r"^\| `([^`]+)` \|")

SUSPICIOUS_VERIFICATION_PHRASES = (
    "requires audit",
    "required before",
    "page-level",
    "edition-level",
    "exact edition",
    "compare edition wording",
    "not yet verified",
    "unverified",
    "wikipedia",
    "current tianyan",
    "local contract",
    "未核验",
    "待核验",
)

COMMON_DECISION_ORDER = """exact question and perspective
-> primary category and redirects
-> primary anchor/useful spirit
-> month/day
-> relevant movement/change
-> Shi/Ying
-> branch structures and hidden spirits
-> six spirits
-> trigram corroboration
-> real facts
-> confidence and resolution cap"""

COMMON_PROHIBITED_SHORTCUTS = (
    "Do not infer gender",
    "Do not infer absence from static lines",
    "Do not infer action, success, or existence from movement alone",
    "Do not derive a modern city",
    "Do not derive an exact date",
)


def _rel(path: Path, skill_root: Path | None = None) -> str:
    if skill_root is None:
        return path.as_posix()
    try:
        return path.relative_to(skill_root).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path, errors: list[str], skill_root: Path | None = None) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"{_rel(path, skill_root)}: missing file")
    except UnicodeDecodeError as exc:
        errors.append(f"{_rel(path, skill_root)}: invalid UTF-8 ({exc})")
    return None


def _section_lines(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    try:
        start = lines.index(heading) + 1
    except ValueError:
        return []

    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return lines[start:end]


def parse_source_records(path: Path) -> dict[str, dict[str, str]]:
    """Parse one source markdown file into source records.

    Structural problems are returned in a synthetic ``"__errors__"`` record so
    callers can keep this public API compact while still reporting accumulated
    validation errors.
    """

    errors: list[str] = []
    text = _read_text(path, errors)
    if text is None:
        return {"__errors__": {"errors": "\n".join(errors)}}

    records: dict[str, dict[str, str]] = {}
    current_id: str | None = None
    current_fields: dict[str, str] = {}

    def finish_record() -> None:
        if current_id is None:
            return
        _validate_source_record(path, current_id, current_fields, errors)
        if current_id in records:
            errors.append(f"{path.as_posix()}: duplicate source ID {current_id}")
        else:
            records[current_id] = dict(current_fields)

    for line_number, line in enumerate(text.splitlines(), start=1):
        heading_match = SOURCE_ID_PATTERN.match(line)
        if heading_match:
            finish_record()
            current_id = heading_match.group(1)
            current_fields = {}
            continue

        if current_id is None:
            continue

        field_match = FIELD_PATTERN.match(line)
        if field_match:
            field_name = field_match.group(1)
            value = field_match.group(2).strip()
            if field_name not in SOURCE_FIELDS:
                errors.append(f"{path.as_posix()}:{line_number}: unknown field {field_name}")
            elif field_name in current_fields:
                errors.append(f"{path.as_posix()}:{line_number}: duplicate field {field_name} in {current_id}")
            elif not value:
                errors.append(f"{path.as_posix()}:{line_number}: empty field {field_name} in {current_id}")
            else:
                current_fields[field_name] = value

    finish_record()

    if errors:
        records["__errors__"] = {"errors": "\n".join(errors)}
    return records


def _validate_source_record(
    path: Path,
    source_id: str,
    fields: dict[str, str],
    errors: list[str],
) -> None:
    for field_name in SOURCE_FIELDS:
        if field_name not in fields:
            errors.append(f"{path.as_posix()}: {source_id} missing field {field_name}")

    for field_name, value in fields.items():
        if field_name not in SOURCE_FIELDS:
            continue
        if not value.strip():
            errors.append(f"{path.as_posix()}: {source_id} empty field {field_name}")

    status = fields.get("Status", "")
    if status and status not in {"A", "B", "C"}:
        errors.append(f"{path.as_posix()}: {source_id} unknown status {status}")
    if status in {"A", "B"}:
        verification_text = f"{fields.get('Locator', '')} {fields.get('Original', '')}".lower()
        for phrase in SUSPICIOUS_VERIFICATION_PHRASES:
            if phrase.lower() in verification_text:
                errors.append(
                    f"{path.as_posix()}: {source_id} status {status} has unverified locator/original phrase {phrase}"
                )
                break
    if not fields.get("Original", "").strip():
        errors.append(f"{path.as_posix()}: {source_id} empty original text")
    if not fields.get("Locator", "").strip():
        errors.append(f"{path.as_posix()}: {source_id} missing locator")


def validate_source_library(skill_root: Path) -> list[str]:
    errors: list[str] = []
    source_root = skill_root / "references" / "sources"
    index_path = source_root / "index.md"
    if not index_path.exists():
        errors.append("references/sources/index.md: missing file")

    all_records: dict[str, dict[str, str]] = {}
    seen_paths: dict[str, str] = {}
    for filename in SOURCE_FILENAMES:
        path = source_root / filename
        if not path.exists():
            errors.append(f"references/sources/{filename}: missing file")
            continue

        records = parse_source_records(path)
        parse_errors = records.pop("__errors__", None)
        if parse_errors:
            for error in parse_errors["errors"].splitlines():
                errors.append(_normalize_path_error(error, skill_root))

        for source_id, fields in records.items():
            rel_path = _rel(path, skill_root)
            if source_id in all_records:
                errors.append(
                    f"{rel_path}: duplicate source ID {source_id} also in {seen_paths[source_id]}"
                )
            else:
                all_records[source_id] = fields
                seen_paths[source_id] = rel_path

    return errors


def _normalize_path_error(error: str, skill_root: Path) -> str:
    prefix = skill_root.as_posix() + "/"
    normalized = error.replace("\\", "/")
    if normalized.startswith(prefix):
        return normalized[len(prefix) :]
    return normalized


def _collect_source_records(skill_root: Path) -> tuple[dict[str, dict[str, str]], list[str]]:
    errors: list[str] = []
    records: dict[str, dict[str, str]] = {}
    source_root = skill_root / "references" / "sources"
    for filename in SOURCE_FILENAMES:
        path = source_root / filename
        if not path.exists():
            continue
        parsed = parse_source_records(path)
        parse_errors = parsed.pop("__errors__", None)
        if parse_errors:
            errors.extend(_normalize_path_error(error, skill_root) for error in parse_errors["errors"].splitlines())
        for source_id, fields in parsed.items():
            if source_id in records:
                errors.append(f"{_rel(path, skill_root)}: duplicate source ID {source_id}")
            else:
                records[source_id] = fields
    return records, errors


def validate_question_module(path: Path, source_records: dict[str, dict[str, str]]) -> list[str]:
    errors: list[str] = []
    text = _read_text(path, errors)
    if text is None:
        return errors

    module_id = path.stem
    for heading in MODULE_HEADINGS:
        if heading not in text.splitlines():
            errors.append(f"{path.as_posix()}: missing heading {heading}")

    category_line = f"- Category ID: {module_id}"
    if category_line not in text.splitlines():
        errors.append(f"{path.as_posix()}: missing exact line {category_line}")

    trigger_bullets = [
        line
        for line in _section_lines(text, "## Trigger Questions")
        if line.strip().startswith("- ") and line.strip()[2:].strip()
    ]
    if len(trigger_bullets) < 3:
        errors.append(f"{path.as_posix()}: expected at least 3 trigger question bullets")

    source_section = "\n".join(_section_lines(text, "## Source Rule IDs"))
    source_ids = SOURCE_REF_PATTERN.findall(source_section)
    if not source_ids:
        errors.append(f"{path.as_posix()}: expected at least 1 source rule ID")

    for source_id in source_ids:
        if source_id not in source_records:
            errors.append(f"{path.as_posix()}: unknown source rule ID {source_id}")
            continue
        if source_records[source_id].get("Status") == "C":
            errors.append(f"{path.as_posix()}: source rule ID {source_id} has status C")

    return errors


def validate_routing_cases(skill_root: Path) -> list[str]:
    errors: list[str] = []
    path = skill_root / "tests" / "question-routing-cases.json"
    text = _read_text(path, errors, skill_root)
    if text is None:
        return errors

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"tests/question-routing-cases.json:{exc.lineno}:{exc.colno}: invalid JSON ({exc.msg})"]

    if data.get("schema_version") != 1:
        errors.append("tests/question-routing-cases.json: schema_version must be 1")

    cases = data.get("cases")
    if not isinstance(cases, list):
        errors.append("tests/question-routing-cases.json: cases must be a list")
        return errors

    if len(cases) != 60:
        errors.append(f"tests/question-routing-cases.json: expected 60 cases, found {len(cases)}")

    seen_ids: set[str] = set()
    seen_questions: set[str] = set()
    primary_counts: Counter[str] = Counter()
    valid_modules = set(MODULE_IDS)

    for index, case in enumerate(cases):
        case_path = f"tests/question-routing-cases.json: cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{case_path}: case must be an object")
            continue

        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"{case_path}: id must be a non-empty string")
        elif case_id in seen_ids:
            errors.append(f"{case_path}: duplicate id {case_id}")
        else:
            seen_ids.add(case_id)

        question = case.get("question")
        if not isinstance(question, str) or not question.strip():
            errors.append(f"{case_path}: question must be a non-empty string")
        elif question in seen_questions:
            errors.append(f"{case_path}: duplicate question {question}")
        else:
            seen_questions.add(question)

        primary = case.get("primary_category")
        if not isinstance(primary, str) or primary not in valid_modules:
            errors.append(f"{case_path}: unknown primary_category {primary!r}")
        else:
            primary_counts[primary] += 1

        secondary = case.get("secondary_categories")
        if not isinstance(secondary, list):
            errors.append(f"{case_path}: secondary_categories must be a list")
            continue
        if len(secondary) > 2:
            errors.append(f"{case_path}: expected zero to two secondary categories")
        secondary_seen: set[str] = set()
        for category in secondary:
            if not isinstance(category, str) or category not in valid_modules:
                errors.append(f"{case_path}: unknown secondary category {category!r}")
                continue
            if category in secondary_seen:
                errors.append(f"{case_path}: duplicate secondary category {category}")
            secondary_seen.add(category)
            if category == primary:
                errors.append(f"{case_path}: primary category repeated as secondary {category}")

    for module_id in MODULE_IDS:
        count = primary_counts[module_id]
        if count != 3:
            errors.append(f"tests/question-routing-cases.json: primary category {module_id} expected 3 cases, found {count}")

    return errors


def validate_question_type_support_files(skill_root: Path) -> list[str]:
    errors: list[str] = []
    question_root = skill_root / "references" / "question-types"
    index_path = question_root / "index.md"
    common_path = question_root / "common-rules.md"

    index_text = _read_text(index_path, errors, skill_root)
    if index_text is not None:
        category_rows: list[str] = []
        for line in index_text.splitlines():
            match = INDEX_ROW_PATTERN.match(line)
            if match:
                category_rows.append(match.group(1))

        counts = Counter(category_rows)
        for module_id in MODULE_IDS:
            if counts[module_id] != 1:
                errors.append(
                    f"references/question-types/index.md: category {module_id} expected 1 index row, found {counts[module_id]}"
                )
            link = f"({module_id}.md)"
            if link not in index_text:
                errors.append(f"references/question-types/index.md: missing module link {link}")

        for category_id in sorted(set(category_rows) - set(MODULE_IDS)):
            errors.append(f"references/question-types/index.md: unknown category row {category_id}")

    common_text = _read_text(common_path, errors, skill_root)
    if common_text is not None:
        normalized_common = common_text.replace("\r\n", "\n")
        if COMMON_DECISION_ORDER not in normalized_common:
            errors.append("references/question-types/common-rules.md: missing mandatory decision order")
        for phrase in COMMON_PROHIBITED_SHORTCUTS:
            if phrase not in common_text:
                errors.append(f"references/question-types/common-rules.md: missing prohibited shortcut phrase {phrase}")

    return errors


def validate_library(skill_root: Path) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_source_library(skill_root))
    source_records, source_parse_errors = _collect_source_records(skill_root)
    errors.extend(source_parse_errors)

    question_root = skill_root / "references" / "question-types"
    errors.extend(validate_question_type_support_files(skill_root))

    for module_id in MODULE_IDS:
        path = question_root / f"{module_id}.md"
        if not path.exists():
            errors.append(f"references/question-types/{module_id}.md: missing file")
            continue
        module_errors = validate_question_module(path, source_records)
        for error in module_errors:
            errors.append(_normalize_path_error(error, skill_root))

    errors.extend(validate_routing_cases(skill_root))
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_library(root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Validated 20 question modules and 60 routing cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
