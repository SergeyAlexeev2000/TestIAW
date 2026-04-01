import os
import re
from pathlib import PureWindowsPath


SEPARATORS_PATTERN = re.compile(r"[._\s]+")
NON_LETTERS_PATTERN = re.compile(r"[^a-z]")


def clean_letters(value: str) -> str:
    return NON_LETTERS_PATTERN.sub("", value.lower())


def split_name_tokens(full_name: str) -> list[str]:
    parts = re.split(r"\s+", full_name.strip())
    tokens = []

    for part in parts:
        cleaned = re.sub(r"[^a-z-]", "", part.lower())
        if cleaned:
            tokens.append(cleaned)

    return tokens


def split_loose_tokens(value: str) -> list[str]:
    parts = SEPARATORS_PATTERN.split(value.strip().lower())
    tokens = []

    for part in parts:
        cleaned = re.sub(r"[^a-z-]", "", part.lower())
        if cleaned:
            tokens.append(cleaned)

    return tokens


def get_email_local_part(email: str) -> str:
    return email.split("@", 1)[0].strip()


def get_file_stem(file_path: str) -> str:
    path = PureWindowsPath(file_path)
    if path.stem:
        return path.stem
    return os.path.splitext(os.path.basename(file_path))[0]


def build_name_keys(full_name: str) -> set[str]:
    raw_tokens = split_name_tokens(full_name)
    plain_tokens = [token.replace("-", "") for token in raw_tokens]

    if not plain_tokens:
        return set()

    first = plain_tokens[0]
    last = plain_tokens[-1]
    initials = "".join(token[0] for token in plain_tokens if token)

    keys = {
        "".join(plain_tokens),
        "_".join(plain_tokens),
        ".".join(plain_tokens),
        " ".join(plain_tokens),
        first + last,
        f"{first}_{last}",
        f"{first}.{last}",
        f"{first} {last}",
        first[0] + last,
        f"{first[0]}_{last}",
        f"{first[0]}.{last}",
        f"{first[0]} {last}",
        initials,
        initials + last,
    }

    if len(plain_tokens) >= 3:
        middle_initials = [token[0] for token in plain_tokens[1:-1] if token]
        if middle_initials:
            keys.add("".join([first[0], *middle_initials, last]))
            keys.add(".".join([first[0], *middle_initials, last]))
            keys.add("_".join([first[0], *middle_initials, last]))

    # отдельная поддержка фамилий с дефисом
    raw_last = raw_tokens[-1]
    if "-" in raw_last:
        last_hyphen = raw_last
        last_underscore = raw_last.replace("-", "_")
        last_dot = raw_last.replace("-", ".")
        last_compact = raw_last.replace("-", "")

        for last_variant in {last_hyphen, last_underscore, last_dot, last_compact}:
            compact_last = clean_letters(last_variant)
            keys.update(
                {
                    f"{first}_{last_variant}",
                    f"{first}.{last_variant}",
                    first + compact_last,
                    first[0] + compact_last,
                    f"{first[0]}_{last_variant}",
                    f"{first[0]}.{last_variant}",
                }
            )

    normalized = set()
    for key in keys:
        key = key.lower()
        normalized.add(key)
        normalized.add(clean_letters(key))
        normalized.add(key.replace("-", "_"))
        normalized.add(key.replace("-", "."))

    return {key for key in normalized if key}


def build_email_keys(email: str) -> set[str]:
    local = get_email_local_part(email).lower()
    parts = split_loose_tokens(local)
    plain_parts = [part.replace("-", "") for part in parts]

    keys = {
        local,
        clean_letters(local),
        local.replace(".", "_"),
        local.replace("_", "."),
        local.replace("-", "_"),
        local.replace("-", "."),
    }

    if parts:
        keys.update(
            {
                "".join(plain_parts),
                "_".join(parts),
                ".".join(parts),
            }
        )

        if len(parts) >= 2:
            first = plain_parts[0]
            last = plain_parts[-1]
            raw_last = parts[-1]

            keys.update(
                {
                    first + last,
                    f"{first}_{raw_last}",
                    f"{first}.{raw_last}",
                    first[0] + last,
                    f"{first[0]}_{raw_last}",
                    f"{first[0]}.{raw_last}",
                }
            )

    return {key for key in keys if key}


def build_file_keys(file_path: str) -> set[str]:
    stem = get_file_stem(file_path).lower()
    parts = split_loose_tokens(stem)
    plain_parts = [part.replace("-", "") for part in parts]

    keys = {
        stem,
        clean_letters(stem),
        stem.replace(".", "_"),
        stem.replace("_", "."),
        stem.replace("-", "_"),
        stem.replace("-", "."),
    }

    if parts:
        keys.update(
            {
                "".join(plain_parts),
                "_".join(parts),
                ".".join(parts),
                " ".join(parts),
            }
        )

        if len(parts) >= 2:
            first = plain_parts[0]
            last = plain_parts[-1]
            raw_last = parts[-1]

            keys.update(
                {
                    first + last,
                    f"{first}_{raw_last}",
                    f"{first}.{raw_last}",
                    first[0] + last,
                    f"{first[0]}_{raw_last}",
                    f"{first[0]}.{raw_last}",
                }
            )

    return {key for key in keys if key}