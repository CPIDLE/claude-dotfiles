# Python CLI Calculator

## Description
A lightweight command-line interface (CLI) tool for performing basic arithmetic operations. This tool allows users to quickly calculate sums, differences, products, and quotients directly from the terminal.

## Installation
1. Ensure you have Python 3.x installed on your system.
2. Save the source code into a file named `calc.py`.
3. No additional dependencies are required.

## Usage Examples

### Basic Operations

**Addition**
```bash
python calc.py add 10 5
# Output: 15
```

**Subtraction**
```bash
python calc.py sub 20 8
# Output: 12
```

**Multiplication**
```bash
python calc.py mul 4 6.5
# Output: 26
```

**Division**
```bash
python calc.py div 100 4
# Output: 25
```

### Error Cases

**Invalid Number Arguments**
```bash
python calc.py add five 3
# Output: Error: arguments must be numbers
```

**Division by Zero**
```bash
python calc.py div 10 0
# Output: Error: division by zero
```

**Unknown Operator**
```bash
python calc.py mod 10 3
# Output: Error: unknown operator mod
```

**Incorrect Argument Count**
```bash
python calc.py add 5
# Output: Usage: python calc.py <op> <n1> <n2>
```

## API Reference

### `format_output(n)`
Handles the presentation of numerical results to the standard output.

- **Parameters**: `n` (numeric) - The result to be printed.
- **Logic**: 
    - Checks if the number is finite and equivalent to its integer representation (e.g., `5.0`).
    - If it is an integer, it prints the value as an `int` to remove trailing zeros.
    - Otherwise, it prints the value as a `float`.

## Limitations
- **Operand Count**: Only supports exactly two operands per command. It cannot evaluate complex expressions like `1 + 2 + 3`.
- **Operator Support**: Limited to the four basic operations: `add`, `sub`, `mul`, and `div`.
- **Floating Point Precision**: Inherits standard Python floating-point precision, which may result in minor rounding inaccuracies for certain decimal operations.
- **Non-Interactive**: Must be executed with all arguments provided; it does not feature an interactive prompt.