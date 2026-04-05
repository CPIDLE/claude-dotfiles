# Python CLI Utility Collection API Reference

This document provides comprehensive API and CLI documentation for a collection of Python utility modules.

## Table of Contents

1. [calc.py - Arithmetic Calculator](#calcpy---arithmetic-calculator)
2. [counter.py - Persistent JSON Counter](#counterpy---persistent-json-counter)
3. [greet.py - Multilingual Greeter](#greetpy---multilingual-greeter)
4. [passgen.py - Secure Password Generator](#passgenpy---secure-password-generator)
5. [temp.py - Temperature Converter](#temppy---temperature-converter)
6. [wc.py - Word Count Utility](#wcpy---word-count-utility)
7. [jsonf.py - JSON Formatter](#jsonfpy---json-formatter)
8. [b64.py - Base64 Encoding Utility](#b64py---base64-encoding-utility)

---

## calc.py - Arithmetic Calculator

### Purpose
Provides basic arithmetic operations (addition, subtraction, multiplication, and division) via the command line.

### CLI Usage
```bash
python calc.py <op> <n1> <n2>
```
*   **op**: The operation to perform. Supported: `add`, `sub`, `mul`, `div`.
*   **n1**: The first operand (number).
*   **n2**: The second operand (number).

### Functions

#### `format_output(n)`
Formats the numeric result for standard output. If the number is an integer, it prints the integer representation; otherwise, it prints the float.
*   **Parameters:**
    *   `n` (float/int): The number to format.
*   **Return Value:** `None` (outputs directly to stdout).

### Error Conditions
*   **Incorrect Arguments:** If fewer or more than 3 arguments are provided, the script prints usage and exits with code 1.
*   **ValueError:** If `n1` or `n2` are not valid numbers, the script prints "Error: arguments must be numbers" and exits with code 1.
*   **Division by Zero:** If `op` is `div` and `n2` is 0, prints "Error: division by zero" and exits with code 1.
*   **Unknown Operator:** If an unsupported operator is provided, prints "Error: unknown operator <op>" and exits with code 1.

### Examples
```bash
python calc.py add 10 5      # Output: 15
python calc.py div 7 2       # Output: 3.5
python calc.py mul 3 4       # Output: 12
```

---

## counter.py - Persistent JSON Counter

### Purpose
Maintains a persistent count across executions by storing the state in a local JSON file.

### CLI Usage
```bash
python counter.py [--reset]
```
*   **--reset**: Resets the counter to 0.

### Functions

#### `main()`
Entry point that handles file I/O and CLI arguments.
*   **Return Value:** `None` (outputs "Count: X" to stdout).

### State Storage
State is stored in a hidden file named `.counter.json` located in the same directory as the script.
*   **Format:** `{"count": <int>}`

### Error Conditions
*   **JSON/IO Error:** If `.counter.json` is corrupted or unreadable, the counter defaults to 0 for the current session.

### Examples
```bash
python counter.py            # Output: Count: 1
python counter.py            # Output: Count: 2
python counter.py --reset    # Output: Count: 0
```

---

## greet.py - Multilingual Greeter

### Purpose
Generates localized greetings for a specified name.

### CLI Usage
```bash
python greet.py [--name NAME] [--lang LANG]
```
*   **--name NAME**: The name of the person to greet (default: "World").
*   **--lang LANG**: The language code. Supported: `en` (English), `zh` (Chinese), `ja` (Japanese). Default: `en`.

### Functions

#### `greet(name="World", lang="en") -> str`
Constructs the greeting string.
*   **Parameters:**
    *   `name` (str): Name to include in the greeting.
    *   `lang` (str): Language code.
*   **Return Value:** `str`: The formatted greeting.
*   **Exceptions:** `ValueError` if the language code is not in the supported list.

### Error Conditions
*   **Unsupported Language:** Providing a language code other than `en`, `zh`, or `ja` results in a `ValueError`, printing an error message to stderr and exiting with code 1.

### Examples
```bash
python greet.py --name Alice --lang zh    # Output: 你好, Alice!
python greet.py --lang ja                 # Output: こんにちは, World!
```

---

## passgen.py - Secure Password Generator

### Purpose
Generates cryptographically strong random passwords.

### CLI Usage
```bash
python passgen.py [--length LENGTH] [--no-symbols]
```
*   **--length LENGTH**: Number of characters in the password (default: 16).
*   **--no-symbols**: Exclude punctuation from the character pool.

### Functions

#### `generate_password(length, use_symbols)`
Generates a random string using the `secrets` module.
*   **Parameters:**
    *   `length` (int): Total character count.
    *   `use_symbols` (bool): Whether to include `string.punctuation`.
*   **Return Value:** `str`: The generated password.

### Error Conditions
*   **Invalid Length:** If `length` is 0 or negative, prints an error to stderr and exits with code 1.

### Examples
```bash
python passgen.py --length 24             # Output: <24-char-random-string>
python passgen.py --no-symbols            # Output: <16-char-alphanumeric-string>
```

---

## temp.py - Temperature Converter

### Purpose
Converts temperatures between Celsius, Fahrenheit, and Kelvin.

### CLI Usage
```bash
python temp.py <mode> <value>
```
*   **mode**: Conversion type. Supported: `c2f` (C to F), `f2c` (F to C), `c2k` (C to K).
*   **value**: Numeric temperature value.

### Functions

#### `c2f(c)`
*   **Parameters:** `c` (float): Celsius.
*   **Return Value:** `float`: Fahrenheit.

#### `f2c(f)`
*   **Parameters:** `f` (float): Fahrenheit.
*   **Return Value:** `float`: Celsius.

#### `c2k(c)`
*   **Parameters:** `c` (float): Celsius.
*   **Return Value:** `float`: Kelvin.

### Error Conditions
*   **Missing Arguments:** Prints usage and exits with code 1.
*   **Invalid Value:** If `value` is not a number, prints "Invalid value" and exits with code 1.
*   **Unknown Mode:** Prints "Unknown mode" if the mode is not recognized.

### Examples
```bash
python temp.py c2f 0         # Output: 32.0
python temp.py c2k 100       # Output: 373.15
```

---

## wc.py - Word Count Utility

### Purpose
Counts lines, words, and characters in a file or from standard input. Similar to the Unix `wc` utility.

### CLI Usage
```bash
python wc.py [FILE]
```
*   **FILE**: Path to the file to analyze. If omitted, reads from `stdin`.

### Input Processing
Uses UTF-8 encoding for file reading. If `stdin` is used, the script waits for an EOF (Ctrl+D / Ctrl+Z).

### Error Conditions
*   **File Not Found:** If the specified file path does not exist, prints an error and exits with code 1.

### Examples
```bash
python wc.py myfile.txt
echo "hello world" | python wc.py
```

---

## jsonf.py - JSON Formatter

### Purpose
Prettifies or minifies JSON data provided as a string or through standard input.

### CLI Usage
```bash
python jsonf.py [json_str] [--compact]
```
*   **json_str**: (Optional) A JSON string to format. If omitted, reads from `stdin`.
*   **--compact**: If flag is present, outputs minified JSON (no spaces/newlines). Otherwise, outputs with 2-space indentation.

### Error Conditions
*   **Invalid JSON:** If the input is not valid JSON, prints `json.JSONDecodeError` details to stderr and exits with code 1.

### Examples
```bash
python jsonf.py '{"a":1,"b":2}'           # Output: Prettified JSON
python jsonf.py '{"a":1}' --compact       # Output: {"a":1}
cat data.json | python jsonf.py           # Formats file content
```

---

## b64.py - Base64 Encoding Utility

### Purpose
Encodes or decodes binary data using Base64, processing data via standard input/output buffers.

### CLI Usage
```bash
python b64.py <encode|decode>
```
*   **encode**: Converts raw input to Base64.
*   **decode**: Converts Base64 input back to raw binary.

### Implementation Details
The module uses `sys.stdin.buffer` and `sys.stdout.buffer` to handle raw binary data safely across platforms.

### Error Conditions
*   **Missing Command:** Prints usage and exits with code 1.
*   **Unknown Command:** Prints "Unknown command" and exits with code 1.
*   **Invalid Base64:** During `decode`, if input is not valid Base64, `base64.b64decode` will raise an error.

### Examples
```bash
echo "hello" | python b64.py encode      # Output: aGVsbG8K
echo "aGVsbG8K" | python b64.py decode   # Output: hello
```