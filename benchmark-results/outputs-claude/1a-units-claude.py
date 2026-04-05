import sys

CONVERSIONS: dict[tuple[str, str], float] = {
    ("km", "miles"): 0.621371,
    ("miles", "km"): 1.60934,
    ("kg", "lbs"): 2.20462,
    ("lbs", "kg"): 0.453592,
    ("liters", "gallons"): 0.264172,
    ("gallons", "liters"): 3.78541,
}


def convert(value: float, from_unit: str, to_unit: str) -> float:
    key = (from_unit.lower(), to_unit.lower())
    if key not in CONVERSIONS:
        print(f"Error: cannot convert '{from_unit}' to '{to_unit}'")
        print(f"Supported: {', '.join(f'{a}->{b}' for a, b in CONVERSIONS)}")
        sys.exit(1)
    return value * CONVERSIONS[key]


def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: python units.py <from_unit> <to_unit> <value>")
        sys.exit(1)

    from_unit, to_unit, raw_value = sys.argv[1], sys.argv[2], sys.argv[3]

    try:
        value = float(raw_value)
    except ValueError:
        print(f"Error: '{raw_value}' is not a valid number")
        sys.exit(1)

    result = convert(value, from_unit, to_unit)
    print(f"{result:.2f}")


if __name__ == "__main__":
    main()
