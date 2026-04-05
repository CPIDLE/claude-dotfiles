import sys

def convert():
    if len(sys.argv) != 4:
        print("Usage: python units.py <from_unit> <to_unit> <value>")
        return

    from_unit = sys.argv[1].lower()
    to_unit = sys.argv[2].lower()
    
    try:
        val = float(sys.argv[3])
    except ValueError:
        print("Error: Value must be a number.")
        return

    conversions = {
        ("km", "miles"): 0.621371,
        ("miles", "km"): 1.60934,
        ("kg", "lbs"): 2.20462,
        ("lbs", "kg"): 0.453592,
        ("liters", "gallons"): 0.264172,
        ("gallons", "liters"): 3.78541
    }

    pair = (from_unit, to_unit)
    if pair in conversions:
        result = val * conversions[pair]
        print(f"{result:.2f}")
    else:
        print(f"Error: Cannot convert from {from_unit} to {to_unit}. Supported pairs: km/miles, kg/lbs, liters/gallons.")

if __name__ == "__main__":
    convert()