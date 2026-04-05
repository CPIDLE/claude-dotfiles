# Calc CLI

A lightweight command-line interface calculator tool that supports basic arithmetic operations.

## Installation

Ensure you have Python 3 installed on your system. No external dependencies are required. Simply download `calc.py` to your local machine.

## Usage

The calculator follows the syntax: `python calc.py <op> <n1> <n2>`

### Operations
* **Addition**: `python calc.py add 5 3` -> `8`
* **Subtraction**: `python calc.py sub 10 4` -> `6`
* **Multiplication**: `python calc.py mul 2 3` -> `6`
* **Division**: `python calc.py div 10 2` -> `5`

### Error Cases
* **Invalid Numbers**: `python calc.py add a 5` -> `Error: arguments must be numbers`
* **Division by Zero**: `python calc.py div 10 0` -> `Error: division by zero`
* **Unknown Operator**: `python calc.py power 2 3` -> `Error: unknown operator power`
* **Invalid Argument Count**: `python calc.py add 1` -> `Usage: python calc.py <op> <n1> <n2>`

## API Reference

### `format_output(n)`

Formats the numeric result for display.

* **Parameters**: 
    * `n` (float/int): The numeric result of the operation.
* **Behavior**:
    * If `n` is a finite integer (e.g., `5.0`), it prints the value as an integer (e.g., `5`).
    * Otherwise (if `n` is a float with decimals or special values like `inf`), it prints the value as-is.

## Limitations

* **Precision**: Uses standard Python `float` types, which are subject to binary floating-point rounding errors. Not suitable for high-precision financial calculations.
* **Overflow**: Extremely large calculations may result in `inf` (infinity) values.
* **Complexity**: Supports only binary operations (two operands). It does not support nested expressions, order of operations (PEMDAS), or scientific functions (e.g., sin, cos, log).