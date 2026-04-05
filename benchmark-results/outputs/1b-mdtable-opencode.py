import sys
import csv

def csv_to_markdown():
    # Read from stdin
    reader = csv.reader(sys.stdin)
    try:
        rows = list(reader)
    except EOFError:
        return

    if not rows:
        return

    # Extract headers and data
    headers = rows[0]
    data = rows[1:]

    # Calculate column widths
    widths = [len(str(h)) for h in headers]
    for row in data:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(str(cell)))
            else:
                # Handle rows with more columns than header
                widths.append(len(str(cell)))

    # Ensure widths match data if data is wider than header
    num_cols = len(widths)

    def format_row(row_data):
        formatted = []
        for i in range(num_cols):
            val = row_data[i] if i < len(row_data) else ""
            formatted.append(f" {str(val).ljust(widths[i])} ")
        return "|" + "|".join(formatted) + "|"

    # Print Header
    print(format_row(headers))
    
    # Print Separator
    sep = "|" + "|".join(["-" * (w + 2) for w in widths]) + "|"
    print(sep)

    # Print Data Rows
    for row in data:
        print(format_row(row))

if __name__ == "__main__":
    csv_to_markdown()