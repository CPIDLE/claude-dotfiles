## [0.2.0] - 2026-04-05

### Added
- Introduced `passgen.py`, a versatile password generation utility. Users can now customize output using the `--length` flag for specific security requirements and the `--no-symbols` flag to ensure compatibility with systems that restrict special characters.
- Added `b64.py` for Base64 encoding and decoding. This tool is optimized for shell pipelines, allowing users to pipe binary or text data directly from `stdin` for seamless integration into automation scripts.

### Changed
- Enhanced `calc.py` robustness by implementing safe handling for mathematical edge cases. Calculations that result in infinity or NaN (Not a Number) no longer trigger an `OverflowError` crash, returning standardized results instead.

### Fixed
- Fixed a concurrency bug in `counter.py` that caused race conditions. The utility now employs proper file locking or atomic writes when updating `.counter.json`, preventing data loss when multiple instances are running simultaneously.