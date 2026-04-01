from app.models import NameEntry, EmailEntry, FileEntry, OutputRecord
from app.normalizer import build_name_keys, build_email_keys, build_file_keys


def make_name_entries(names: list[str]) -> list[NameEntry]:
    return [NameEntry(raw=name, keys=build_name_keys(name)) for name in names]


def make_email_entries(emails: list[str]) -> list[EmailEntry]:
    return [EmailEntry(raw=email, keys=build_email_keys(email)) for email in emails]


def make_file_entries(file_paths: list[str]) -> list[FileEntry]:
    return [FileEntry(raw=path, keys=build_file_keys(path)) for path in file_paths]


def score_match(left_keys: set[str], right_keys: set[str]) -> int:
    return len(left_keys & right_keys)


def find_best_unique_match(source_keys: set[str], candidates: list, used_raw_values: set[str]):
    scored = []

    for candidate in candidates:
        if candidate.raw in used_raw_values:
            continue

        score = score_match(source_keys, candidate.keys)
        if score > 0:
            scored.append((score, candidate))

    if not scored:
        return None

    scored.sort(key=lambda item: item[0], reverse=True)

    best_score = scored[0][0]
    best_candidates = [candidate for score, candidate in scored if score == best_score]

    if len(best_candidates) == 1:
        return best_candidates[0]

    return None


def build_output_records(
    names: list[str],
    emails: list[str],
    file_paths: list[str],
) -> list[OutputRecord]:
    name_entries = make_name_entries(names)
    email_entries = make_email_entries(emails)
    file_entries = make_file_entries(file_paths)

    used_emails: set[str] = set()
    used_files: set[str] = set()
    results: list[OutputRecord] = []

    for name_entry in name_entries:
        matched_email = find_best_unique_match(name_entry.keys, email_entries, used_emails)
        matched_file = find_best_unique_match(name_entry.keys, file_entries, used_files)

        if matched_email:
            used_emails.add(matched_email.raw)

        if matched_file:
            used_files.add(matched_file.raw)

        results.append(
            OutputRecord(
                full_name=name_entry.raw,
                email=matched_email.raw if matched_email else None,
                file_path=matched_file.raw if matched_file else None,
            )
        )

    for email_entry in email_entries:
        if email_entry.raw not in used_emails:
            results.append(
                OutputRecord(
                    full_name=None,
                    email=email_entry.raw,
                    file_path=None,
                )
            )

    for file_entry in file_entries:
        if file_entry.raw not in used_files:
            results.append(
                OutputRecord(
                    full_name=None,
                    email=None,
                    file_path=file_entry.raw,
                )
            )

    return results