from app.matcher import build_output_records


def test_build_output_records_happy_path():
    names = ["John Stone", "Jane Meldrum"]
    emails = [
        "J.Stone@dundermifflin.com",
        "J_Meldrum@dundermifflin.com",
    ]
    files = [
        r"C:\FirstGroup\John_Stone.pdf",
        r"C:\Second Group\Jane_Meldrum.xml",
    ]

    records = build_output_records(names, emails, files)

    john_record = next(r for r in records if r.full_name == "John Stone")
    jane_record = next(r for r in records if r.full_name == "Jane Meldrum")

    assert john_record.email == "J.Stone@dundermifflin.com"
    assert john_record.file_path == r"C:\FirstGroup\John_Stone.pdf"

    assert jane_record.email == "J_Meldrum@dundermifflin.com"
    assert jane_record.file_path == r"C:\Second Group\Jane_Meldrum.xml"


def test_build_output_records_missing_file():
    names = ["Ang Li"]
    emails = ["A_Li@dundermifflin.com"]
    files = []

    records = build_output_records(names, emails, files)
    record = records[0]

    assert record.full_name == "Ang Li"
    assert record.email == "A_Li@dundermifflin.com"
    assert record.file_path is None


def test_build_output_records_unmatched_email():
    names = []
    emails = ["J.Osbourne@dundermifflin.com"]
    files = []

    records = build_output_records(names, emails, files)

    assert len(records) == 1
    assert records[0].full_name is None
    assert records[0].email == "J.Osbourne@dundermifflin.com"
    assert records[0].file_path is None


def test_build_output_records_unmatched_file():
    names = []
    emails = []
    files = [r"C:\Misc\Unknown_User.pdf"]

    records = build_output_records(names, emails, files)

    assert len(records) == 1
    assert records[0].full_name is None
    assert records[0].email is None
    assert records[0].file_path == r"C:\Misc\Unknown_User.pdf"