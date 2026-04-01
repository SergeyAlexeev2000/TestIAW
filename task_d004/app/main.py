from pathlib import Path

from app.matcher import build_output_records
from app.models import OutputRecord
from app.parser import read_lines
from app.writer import write_json, write_tuples


def sort_records(records: list[OutputRecord]) -> list[OutputRecord]:
    return sorted(
        records,
        key=lambda r: (
            r.full_name is None,
            r.full_name or "",
            r.email or "",
            r.file_path or "",
        ),
    )


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent

    names_path = base_dir / "input_data" / "Users names.txt"
    emails_path = base_dir / "input_data" / "List of e-mails.txt"
    files_path = base_dir / "input_data" / "List_of_files.txt"

    json_output_path = base_dir / "output" / "result.json"
    tuples_output_path = base_dir / "output" / "result_tuples.txt"

    names = read_lines(names_path)
    emails = read_lines(emails_path)
    file_paths = read_lines(files_path)

    records = build_output_records(
        names=names,
        emails=emails,
        file_paths=file_paths,
    )

    records = sort_records(records)

    write_json(records, json_output_path)
    write_tuples(records, tuples_output_path)

    print(f"Done. JSON result saved to: {json_output_path}")
    print(f"Done. Tuple result saved to: {tuples_output_path}")


if __name__ == "__main__":
    main()