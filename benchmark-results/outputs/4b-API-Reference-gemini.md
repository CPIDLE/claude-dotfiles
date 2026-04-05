# CLI Modules API Documentation

## Table of Contents
1. [calc.py](#calcpy)
2. [counter.py](#counterpy)
3. [greet.py](#greetpy)
4. [passgen.py](#passgenpy)
5. [temp.py](#temppy)
6. [wc.py](#wcpy)
7. [jsonf.py](#jsonfpy)
8. [b64.py](#b64py)

---

## calc.py
**Purpose**: A simple command-line calculator for basic arithmetic operations.

**CLI Usage**: `python calc.py <op> <n1> <n2>`
*   `op`: Operator (`add`, `sub`, `mul`, `div`)
*   `n1`, `n2`: Numbers to operate on.

**Functions**
*   `format_output(n: float)`: Prints the result. If `n` is a whole number, it is printed as an integer; otherwise, it is printed as a float.
*   `main()`: Handles CLI argument parsing and execution logic.

**Error Conditions**
*   Prints usage/error messages and exits with code 1 if arguments are invalid, non-numeric, or if division by zero is attempted.

**Example**
```bash
python calc.py add 5 3   # Output: 8
python calc.py div 10 2  # Output: 5
```

---

## counter.py
**Purpose**: Persists and increments a counter in a local `.counter.json` file.

**CLI Usage**: `python counter.py [--reset]`
*   `--reset`: Resets the count to 0 instead of incrementing.

**Functions**
*   `main()`: Reads the state from the disk, performs the calculation, and saves the new state.

**Error Conditions**
*   If the JSON file is corrupt, the counter defaults to 0.

---

## greet.py
**Purpose**: Provides multilingual greetings based on a name and language code.

**CLI Usage**: `python greet.py [--name <name>] [--lang <en|zh|ja>]`

**Functions**
*   `greet(name: str = "World", lang: str = "en") -> str`:
    *   **Parameters**: `name` (the target), `lang` (language key).
    *   **Returns**: Formatted greeting string.
    *   **Raises**: `ValueError` if the language code is not supported.

**Example**
```bash
python greet.py --name Alice --lang zh # Output: 你好, Alice!
```

---

## passgen.py
**Purpose**: Generates a cryptographically secure random password.

**CLI Usage**: `python passgen.py [--length <int>] [--no-symbols]`

**Functions**
*   `generate_password(length: int, use_symbols: bool) -> str`:
    *   **Parameters**: `length` (password length), `use_symbols` (boolean flag to include symbols).
    *   **Returns**: Random string of characters.

**Error Conditions**
*   Exits with status 1 if `length` is $\leq 0$.

---

## temp.py
**Purpose**: Converts temperature values between units.

**CLI Usage**: `python temp.py <mode> <value>`
*   Modes: `c2f` (Celsius to Fahrenheit), `f2c` (Fahrenheit to Celsius), `c2k` (Celsius to Kelvin).

**Functions**
*   `c2f(c)`, `f2c(f)`, `c2k(c)`: Mathematical conversion functions.

---

## wc.py
**Purpose**: Counts lines, words, and characters in a file or stdin.

**CLI Usage**: `python wc.py [FILE]`

**Error Conditions**
*   Exits 1 if the file path provided does not exist.

---

## jsonf.py
**Purpose**: Formats or compresses JSON input.

**CLI Usage**: `python jsonf.py [JSON_STRING] [--compact]`

**Functions**
*   `main()`: Parses JSON from either a positional argument or `sys.stdin`.

**Error Conditions**
*   Exits 1 with an error message if the input is not valid JSON.

---

## b64.py
**Purpose**: Base64 encoding/decoding utility for binary streams.

**CLI Usage**: `echo "text" | python b64.py [encode|decode]`

**Functions**
*   `main()`: Reads bytes from `sys.stdin.buffer` and writes result to `sys.stdout.buffer`.

**Error Conditions**
*   Exits 1 if invalid command is provided or no command is given.