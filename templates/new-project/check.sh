#!/usr/bin/env bash
# Project lint/test gate — runs after Write/Edit/MultiEdit (PostToolUse hook).
# Exit non-zero blocks the edit. /pm new auto-fills <TEST_CMD>; edit as the project grows.
set -e

<TEST_CMD>
