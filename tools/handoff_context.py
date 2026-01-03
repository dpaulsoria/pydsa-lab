from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read_text(path: Path, limit: int = 4000) -> str:
    try:
        txt = path.read_text(encoding="utf-8", errors="replace")
        if len(txt) > limit:
            return txt[:limit] + "\n... (truncado)\n"
        return txt
    except Exception as e:
        return f"<no se pudo leer {path}: {e}>"


def _list_py_files(base: Path) -> list[str]:
    if not base.exists():
        return []
    out: list[str] = []
    for p in sorted(base.rglob("*.py")):
        rel = p.relative_to(ROOT).as_posix()
        out.append(rel)
    return out


def main() -> None:
    print("=== PyDSA Lab — HANDOFF CONTEXT ===")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Root: {ROOT}")
    print()

    # archivos clave (truncados)
    key_files = [
        ROOT / "README.md",
        ROOT / "pyproject.toml",
        ROOT / "app.py",
        ROOT / "core" / "ui" / "sidebar.py",
        ROOT / "core" / "stepper.py",
    ]

    print("=== Key files (preview) ===")
    for f in key_files:
        print(f"\n--- {f.relative_to(ROOT).as_posix()} ---")
        print(_read_text(f, limit=2500))
    print()

    # estructura por carpetas
    print("=== Python files inventory ===")
    for folder in ["pages", "core/structures", "core/algos", "core/render", "tests"]:
        base = ROOT / folder
        files = _list_py_files(base)
        print(f"\n[{folder}] ({len(files)})")
        for rel in files[:120]:
            print(f" - {rel}")
        if len(files) > 120:
            print(" - ... (más archivos)")
    print()

    # quick todo scan
    print("=== TODO/FIXME scan (top hits) ===")
    hits = 0
    for p in (ROOT / "core").rglob("*.py"):
        txt = _read_text(p, limit=200000)
        for i, line in enumerate(txt.splitlines(), start=1):
            if "TODO" in line or "FIXME" in line:
                rel = p.relative_to(ROOT).as_posix()
                print(f"{rel}:{i}: {line.strip()}")
                hits += 1
                if hits >= 40:
                    print("... (limitado a 40 hits)")
                    return


if __name__ == "__main__":
    # evita romper si ejecutas desde otro cwd
    os.chdir(ROOT)
    main()
