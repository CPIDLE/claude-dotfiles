# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.2.0] - 2026-04-05

### Added

- **passgen.py** — A cryptographically secure password generator using `secrets`. Supports `--length` (default 16) to control output length and `--no-symbols` to restrict the character set to letters and digits only. Useful for generating passwords that comply with systems that reject special characters.

- **b64.py** — A Base64 encoder/decoder that reads from stdin, making it composable in shell pipelines. `echo "hello" | python b64.py encode` produces the Base64 string; pipe it back through `decode` to recover the original. Handles binary data correctly via `sys.stdin.buffer`.

### Changed

- **calc.py** now gracefully handles `infinity` and `NaN` results instead of crashing with an `OverflowError`. Previously, operations like `1e308 * 10` would raise an unhandled exception; they now print `inf` via the updated `format_output()` function, which checks `math.isfinite()` before formatting.

### Fixed

- **counter.py** — Resolved a race condition that occurred when multiple processes wrote to `.counter.json` simultaneously. Concurrent increments could silently lose counts or corrupt the JSON file. The counter now uses atomic file operations to ensure each invocation reads and writes a consistent state.
