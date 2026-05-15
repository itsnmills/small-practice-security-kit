from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path


EXCHANGE_FIELDS = [
    "source_repo",
    "source_artifact",
    "item_id",
    "module",
    "title",
    "status",
    "risk",
    "owner",
    "evidence_needed",
    "evidence_reference",
    "source_mapping",
    "next_review_due",
    "notes",
]


@dataclass
class ExchangeRecord:
    source_repo: str
    source_artifact: str
    item_id: str
    module: str
    title: str
    status: str
    risk: str
    owner: str
    evidence_needed: str
    evidence_reference: str
    source_mapping: str
    next_review_due: str
    notes: str

    def as_row(self) -> dict[str, str]:
        return asdict(self)


def validate_exchange_records(records: list[ExchangeRecord]) -> None:
    for index, record in enumerate(records):
        row = record.as_row()
        missing = [field for field in EXCHANGE_FIELDS if not str(row.get(field, "")).strip()]
        if missing:
            raise ValueError(f"exchange record {index} missing required field(s): {', '.join(missing)}")


def records_to_csv(records: list[ExchangeRecord], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXCHANGE_FIELDS, lineterminator="\n")
        writer.writeheader()
        for record in records:
            writer.writerow(record.as_row())


def records_from_csv(path: Path) -> list[ExchangeRecord]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [ExchangeRecord(**{field: row.get(field, "") for field in EXCHANGE_FIELDS}) for row in reader]


def records_to_markdown(records: list[ExchangeRecord], path: Path, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {title}",
        "",
        "| Item ID | Module | Title | Risk | Owner | Evidence Needed | Evidence Reference |",
        "|---|---|---|---|---|---|---|",
    ]
    for record in records:
        lines.append(
            f"| {record.item_id} | {record.module} | {record.title} | {record.risk} | "
            f"{record.owner} | {record.evidence_needed} | {record.evidence_reference} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
