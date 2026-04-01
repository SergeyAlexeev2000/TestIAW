from pathlib import Path

def read_lines(path: str | Path) -> list[str]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
    
    