## [0.2.0] - 2023-10-27

### Added
- **Password Generator (`passgen.py`):** You can now generate secure, random passwords directly from the CLI. Use the `--length` flag to specify character count and the `--no-symbols` flag to exclude special characters if your target system has specific requirements.
- **Base64 Utility (`b64.py`):** A new tool for encoding and decoding strings to Base64. It is designed to play nicely with your shell, featuring full support for stdin piping to easily process data streams from other commands.

### Changed
- **Calculator (`calc.py`):** Improved robustness for mathematical operations. The calculator now gracefully handles edge cases like infinity and NaN (Not-a-Number) instead of raising an `OverflowError`, ensuring your scripts don't crash when encountering extreme values.

### Fixed
- **Counter (`counter.py`):** Resolved a race condition that occurred when multiple instances of the script attempted to write to `.counter.json` simultaneously. The update implements file locking to ensure data integrity and prevent corruption during high-concurrency usage.