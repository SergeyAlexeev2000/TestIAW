from __future__ import annotations

from pathlib import Path
from typing import Iterable

EXCLUDED_DIRS = {
    '.git',
    '.idea',
    '.vscode',
    '.pytest_cache',
    '__pycache__',
    'venv',
    '.venv',
    'node_modules',
    'dist',
    'build',
}

INCLUDED_SUFFIXES = {
    '.py',
    '.txt',
    '.md',
    '.rst',
    '.ini',
    '.toml',
    '.yaml',
    '.yml',
    '.json',
    '.csv',
}

EXCLUDED_FILENAMES = {
    '.DS_Store',
}


def iter_project_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob('*')):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.is_dir():
            continue
        if path.name in EXCLUDED_FILENAMES:
            continue
        if path.suffix.lower() not in INCLUDED_SUFFIXES:
            continue
        yield path


def build_tree(root: Path) -> str:
    lines: list[str] = [f'{root.name}/']

    def walk(directory: Path, prefix: str = '') -> None:
        entries = [
            p for p in sorted(directory.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
            if p.name not in EXCLUDED_FILENAMES and p.name not in EXCLUDED_DIRS
        ]
        for index, entry in enumerate(entries):
            connector = '└── ' if index == len(entries) - 1 else '├── '
            lines.append(f'{prefix}{connector}{entry.name}{"/" if entry.is_dir() else ""}')
            if entry.is_dir():
                extension = '    ' if index == len(entries) - 1 else '│   '
                walk(entry, prefix + extension)

    walk(root)
    return '\n'.join(lines)


def dump_project(root: Path, output_path: Path) -> None:
    files = list(iter_project_files(root))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open('w', encoding='utf-8') as f:
        f.write(f'PROJECT ROOT: {root}\n\n')
        f.write('PROJECT TREE\n')
        f.write('=' * 80 + '\n')
        f.write(build_tree(root))
        f.write('\n\n')

        for file_path in files:
            relative = file_path.relative_to(root)
            f.write('=' * 80 + '\n')
            f.write(f'FILE: {relative}\n')
            f.write('=' * 80 + '\n')
            try:
                content = file_path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                content = file_path.read_text(encoding='utf-8', errors='replace')
            f.write(content)
            if not content.endswith('\n'):
                f.write('\n')
            f.write('\n')


if __name__ == '__main__':
    project_root = Path.cwd()
    output_file = project_root / 'project_dump.txt'
    dump_project(project_root, output_file)
    print(f'Done. Dump saved to: {output_file}')
