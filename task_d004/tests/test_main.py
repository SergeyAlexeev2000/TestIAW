import json
from pathlib import Path

from app.matcher import build_output_records
from app.writer import write_json


def test_end_to_end(tmp_path: Path):
    names = ["John Stone"]
    emails = ["J.Stone@dundermifflin.com"]
    files = [r"C:\FirstGroup\John_Stone.pdf"]

    records = build_output_records(names, emails, files)

    out_file = tmp_path / "result.json"
    write_json(records, out_file)

    assert out_file.exists()

    payload = json.loads(out_file.read_text(encoding="utf-8"))
    assert len(payload) == 1
    assert payload[0]["full_name"] == "John Stone"
    assert payload[0]["email"] == "J.Stone@dundermifflin.com"
    assert payload[0]["file_path"] == r"C:\FirstGroup\John_Stone.pdf"