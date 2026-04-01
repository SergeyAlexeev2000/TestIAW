import json
from dataclasses import asdict
from pathlib import Path

from app.models import OutputRecord


def write_json(records: list[OutputRecord], output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = [asdict(record) for record in records]

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(
            payload,
            f,
            ensure_ascii=False,
            indent=2,
            sort_keys=False,
        )
        f.write("\n")


def write_tuples(records: list[OutputRecord], output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = [
        (record.full_name, record.email, record.file_path)
        for record in records
    ]

    with output_path.open("w", encoding="utf-8") as f:
        f.write("[\n")
        for index, item in enumerate(payload):
            suffix = "," if index < len(payload) - 1 else ""
            f.write(f"    {item!r}{suffix}\n")
        f.write("]\n")