# CLI Toolkit API Reference

## Table of Contents

- [calc.py — Calculator](#calcpy)
- [counter.py — JSON Counter](#counterpy)
- [greet.py — Multilingual Greeting](#greetpy)
- [passgen.py — Password Generator](#passgenpy)
- [temp.py — Temperature Converter](#temppy)
- [wc.py — Word Counter](#wcpy)
- [jsonf.py — JSON Formatter](#jsonfpy)
- [b64.py — Base64 Encoder/Decoder](#b64py)

---

## calc.py

Basic four-operation calculator.

### CLI Usage

```bash
python calc.py <op> <n1> <n2>
```

Where `op` is one of: `add`, `sub`, `mul`, `div`.

### Functions

#### `format_output(n: float) -> None`

Prints `n` as an integer if it has no fractional part (e.g., `5` not `5.0`), otherwise prints the float directly. Handles `inf` and `nan` gracefully via `math.isfinite()`.

#### `main() -> None`

Parses CLI arguments, validates operator and numeric inputs, performs the operation, and calls `format_output`.

### Error Conditions

| Condition | Output | Exit Code |
|---|---|---|
| Wrong argument count | Usage message | 1 |
| Non-numeric arguments | `Error: arguments must be numbers` | 1 |
| Unknown operator | `Error: unknown operator <op>` | 1 |
| Division by zero | `Error: division by zero` | 1 |

### Example

```bash
$ python calc.py add 2 3
5
$ python calc.py div 10 3
3.3333333333333335
```

---

## counter.py

Persistent JSON counter that increments on each invocation.

### CLI Usage

```bash
python counter.py           # increment and print
python counter.py --reset   # reset to 0
```

State is stored in `.counter.json` alongside the script.

### Functions

#### `main() -> None`

Reads `.counter.json`, increments (or resets) the count, writes back, and prints `Count: N`. Handles missing or corrupted JSON files by resetting to 0.

### Error Conditions

| Condition | Behavior |
|---|---|
| `.counter.json` missing | Starts from 0 |
| `.counter.json` corrupted | Resets to 0 |
| File permission error | Unhandled (raises IOError) |

### Example

```bash
$ python counter.py
Count: 1
$ python counter.py
Count: 2
$ python counter.py --reset
Count: 0
```

---

## greet.py

Multilingual greeting CLI. Shares the pattern of argparse-based entry point with [passgen.py](#passgenpy).

### CLI Usage

```bash
python greet.py --name Alice --lang zh
```

### Functions

#### `greet(name: str = "World", lang: str = "en") -> str`

Returns a greeting string. Raises `ValueError` if `lang` is not in the supported set.

**Parameters:**
- `name` — Name to greet (default: `"World"`)
- `lang` — Language code: `en`, `zh`, `ja` (default: `"en"`)

**Returns:** `str` — e.g., `"Hello, Alice!"`

#### `main() -> None`

argparse CLI wrapper. Prints the greeting or exits with code 1 on unsupported language.

### Error Conditions

| Condition | Output | Exit Code |
|---|---|---|
| Unsupported language | `Error: Unsupported language code: <lang>` (stderr) | 1 |

### Example

```bash
$ python greet.py --name Alice --lang ja
こんにちは, Alice!
```

---

## passgen.py

Cryptographically secure password generator using `secrets`. Shares argparse pattern with [greet.py](#greetpy).

### CLI Usage

```bash
python passgen.py --length 24
python passgen.py --no-symbols
```

### Functions

#### `generate_password(length: int, use_symbols: bool) -> str`

Generates a random password from `ascii_letters + digits` (+ `punctuation` if `use_symbols`).

**Parameters:**
- `length` — Number of characters
- `use_symbols` — Whether to include `string.punctuation`

**Returns:** `str` — The generated password.

#### `main() -> None`

argparse CLI wrapper. Exits with code 1 if `length <= 0`.

### Error Conditions

| Condition | Output | Exit Code |
|---|---|---|
| `--length 0` or negative | `Error: Length must be greater than 0` (stderr) | 1 |

### Example

```bash
$ python passgen.py --length 12 --no-symbols
Abc123Xyz789
```

---

## temp.py

Temperature converter between Celsius, Fahrenheit, and Kelvin.

### CLI Usage

```bash
python temp.py <mode> <value>
```

Where `mode` is one of: `c2f`, `f2c`, `c2k`.

### Functions

#### `c2f(c: float) -> float`

Celsius to Fahrenheit: `(c * 9/5) + 32`

#### `f2c(f: float) -> float`

Fahrenheit to Celsius: `(f - 32) * 5/9`

#### `c2k(c: float) -> float`

Celsius to Kelvin: `c + 273.15`

#### `main() -> None`

Parses CLI arguments, dispatches to the correct conversion function, and prints the result.

### Error Conditions

| Condition | Output | Exit Code |
|---|---|---|
| Too few arguments | Usage message | 1 |
| Non-numeric value | `Invalid value` | 1 |
| Unknown mode | `Unknown mode: <mode>` | 1 |

### Example

```bash
$ python temp.py c2f 100
212.0
$ python temp.py f2c 32
0.0
```

---

## wc.py

Word, line, and character counter. Reads from file argument or stdin. Shares the stdin-reading pattern with [b64.py](#b64py) and [jsonf.py](#jsonfpy).

### CLI Usage

```bash
python wc.py file.txt        # from file
echo "hello world" | python wc.py  # from stdin
```

### Functions

#### `main() -> None`

Reads input from file (first argument) or stdin. Prints line count, word count, and character count.

### Error Conditions

| Condition | Output | Exit Code |
|---|---|---|
| No file and no stdin pipe | Usage message | 1 |
| File not found | `Error: <path> not found` | 1 |

### Example

```bash
$ echo "hello world" | python wc.py
Lines: 1
Words: 2
Characters: 12
```

---

## jsonf.py

JSON pretty-printer / compactor. Reads from argument or stdin. Shares stdin pattern with [wc.py](#wcpy) and [b64.py](#b64py).

### CLI Usage

```bash
echo '{"a":1}' | python jsonf.py
python jsonf.py '{"a":1}' --compact
```

### Functions

#### `main() -> None`

Parses JSON from argument or stdin. Outputs pretty-printed (2-space indent) by default, or compact with `--compact`.

### Error Conditions

| Condition | Output | Exit Code |
|---|---|---|
| Invalid JSON | `Error: Invalid JSON input - <detail>` (stderr) | 1 |
| Empty input | No output, exit 0 | 0 |

### Example

```bash
$ echo '{"name":"Alice","age":30}' | python jsonf.py
{
  "name": "Alice",
  "age": 30
}
```

---

## b64.py

Base64 encoder/decoder. Reads from stdin (binary-safe). Shares stdin pattern with [wc.py](#wcpy) and [jsonf.py](#jsonfpy).

### CLI Usage

```bash
echo "hello" | python b64.py encode
echo "aGVsbG8K" | python b64.py decode
```

### Functions

#### `main() -> None`

Reads binary data from `sys.stdin.buffer`. `encode` outputs Base64 with trailing newline. `decode` outputs raw bytes.

### Error Conditions

| Condition | Output | Exit Code |
|---|---|---|
| No command argument | Usage message | 1 |
| Unknown command | `Unknown command: <cmd>` + usage | 1 |
| Invalid Base64 on decode | Unhandled `binascii.Error` | 1 |

### Example

```bash
$ echo "hello" | python b64.py encode
aGVsbG8K
$ echo "aGVsbG8K" | python b64.py decode
hello
```

---

## Shared Patterns

Several modules share common design patterns:

| Pattern | Modules |
|---|---|
| **stdin pipe input** | wc.py, jsonf.py, b64.py |
| **argparse CLI** | greet.py, passgen.py, counter.py, jsonf.py |
| **positional args + sys.argv** | calc.py, temp.py, b64.py, wc.py |
| **sys.exit(1) on error** | All modules |
