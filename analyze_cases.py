"""Resumen operativo de tickets de soporte desde un archivo CSV."""

from __future__ import annotations

import csv
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

REQUIRED_COLUMNS = {"id", "opened_at", "closed_at", "status", "priority", "category"}


def parse_date(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def main(path: Path) -> None:
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            raise SystemExit(f"Faltan columnas: {', '.join(sorted(missing))}")
        cases = list(reader)
    if not cases:
        raise SystemExit("El CSV no contiene tickets.")
    priorities = Counter(case["priority"].lower() for case in cases)
    categories = Counter(case["category"].lower() for case in cases)
    closed = [case for case in cases if case["status"].lower() == "closed" and case["closed_at"]]
    durations = [(parse_date(case["closed_at"]) - parse_date(case["opened_at"])).total_seconds() / 3600 for case in closed]
    print(f"TICKETS ANALIZADOS: {len(cases)}")
    print(f"CERRADOS: {len(closed)} ({len(closed) / len(cases) * 100:.0f}%)")
    if durations:
        print(f"RESOLUCIÓN PROMEDIO: {sum(durations) / len(durations):.1f} h")
    print("\nPOR PRIORIDAD")
    for name, count in priorities.most_common(): print(f"- {name}: {count}")
    print("\nPOR CATEGORÍA")
    for name, count in categories.most_common(): print(f"- {name}: {count}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python analyze_cases.py tickets.csv")
    main(Path(sys.argv[1]))
