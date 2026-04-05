import sys

def convert():
    if len(sys.argv) != 4:
        print("Usage: python units.py <from_unit> <to_unit> <value>")
        sys.exit(1)

    u_from, u_to, val_str = sys.argv[1].lower(), sys.argv[2].lower(), sys.argv[3]

    try:
        val = float(val_str)
    except ValueError:
        print("Error: Value must be a number.")
        sys.exit(1)

    conversions = {
        ('km', 'miles'): lambda x: x * 0.621371,
        ('miles', 'km'): lambda x: x / 0.621371,
        ('kg', 'lbs'): lambda x: x * 2.20462,
        ('lbs', 'kg'): lambda x: x / 2.20462,
        ('liters', 'gallons'): lambda x: x * 0.264172,
        ('gallons', 'liters'): lambda x: x / 0.264172
    }

    if (u_from, u_to) in conversions:
        result = conversions[(u_from, u_to)](val)
        print(f"{result:.2f}")
    else:
        print(f"Error: Invalid unit conversion from {u_from} to {u_to}.")
        sys.exit(1)

if __name__ == "__main__":
    convert()