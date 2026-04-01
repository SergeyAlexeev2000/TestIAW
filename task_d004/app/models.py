from dataclasses import dataclass
from typing import Optional, Set

@dataclass(frozen=True)
class NameEntry:
    raw: str
    keys: Set[str]

@dataclass(frozen=True)
class EmailEntry:
    raw: str
    keys: Set[str]

@dataclass(frozen=True)
class FileEntry:
    raw: str
    keys: Set[str]

@dataclass(frozen=True)
class OutputRecord:
    full_name: Optional[str]
    email: Optional[str]
    file_path: Optional[str]