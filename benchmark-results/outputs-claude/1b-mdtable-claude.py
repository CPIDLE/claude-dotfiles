import csv
import sys


def main() -> None:
    data = sys.stdin.read()
    if not data.strip():
        return

    reader = csv.reader(data.strip().splitlines())
    rows = list(reader)
    if not rows:
        return

    col_widths = [max(len(row[i]) if i < len(row) else 0 for row in rows) for i in range(len(rows[0]))]

    def fmt_row(row: list[str]) -> str:
        cells = [cell.ljust(w) for cell, w in zip(row, col_widths)]
        return "| " + " | ".join(cells) + " |"

    print(fmt_row(rows[0]))
    print("| " + " | ".join("-" * w for w in col_widths) + " |")
    for row in rows[1:]:
        print(fmt_row(row))


if __name__ == "__main__":
    main()
