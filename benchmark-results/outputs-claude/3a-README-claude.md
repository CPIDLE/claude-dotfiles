# calc.py

A simple command-line calculator supporting four basic arithmetic operations.

## Installation

No dependencies required. Python 3.6+.

```bash
git clone <repo-url>
cd <repo>/dual-engine/examples
```

## Usage

```bash
python calc.py <operation> <num1> <num2>
```

### Operations

| Operation | Command | Example |
|---|---|---|
| Addition | `add` | `python calc.py add 2 3` → `5` |
| Subtraction | `sub` | `python calc.py sub 10 3` → `7` |
| Multiplication | `mul` | `python calc.py mul 4 2.5` → `10.0` |
| Division | `div` | `python calc.py div 10 3` → `3.3333333333333335` |

### Error Cases

```bash
# Division by zero
python calc.py div 10 0
# Error: division by zero (exit 1)

# Invalid operator
python calc.py mod 10 3
# Error: unknown operator mod (exit 1)

# Non-numeric arguments
python calc.py add foo bar
# Error: arguments must be numbers (exit 1)

# Wrong argument count
python calc.py add 1
# Usage: python calc.py <op> <n1> <n2> (exit 1)
```

## API Reference

### `format_output(n)`

Formats and prints a numeric result to stdout.

**Parameters:**
- `n` (float): The number to format.

**Behavior:**
- If `n` is finite and equal to its integer value → prints as `int` (e.g., `5` not `5.0`)
- Otherwise → prints the float directly (e.g., `3.3333333333333335`, `inf`, `nan`)

**Examples:**
```python
format_output(5.0)   # prints: 5
format_output(3.14)  # prints: 3.14
format_output(float('inf'))  # prints: inf
```

### `main()`

CLI entry point. Parses `sys.argv`, validates inputs, performs the operation, and calls `format_output()`.

## Limitations

- Only supports two operands per invocation (no chaining like `2 + 3 * 4`)
- Four operators only: `add`, `sub`, `mul`, `div`
- Float precision limited to Python's IEEE 754 double-precision
- No expression parsing — operator must be a separate positional argument
- Large multiplications may produce `inf` (handled gracefully via `format_output`)
