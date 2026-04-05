import csv
import sys

def main():
    reader = csv.reader(sys.stdin)
    rows = list(reader)
    
    if not rows:
        return

    header = rows[0]
    data = rows[1:]

    def format_row(row):
        return "| " + " | ".join(cell.strip() for cell in row) + " |"

    print(format_row(header))
    print("| " + " | ".join(["---"] * len(header)) + " |")
    
    for row in data:
        print(format_row(row))

if __name__ == "__main__":
    main()