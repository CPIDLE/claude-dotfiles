#!/bin/bash
# Claude Code Status Line
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULT=$(node "$SCRIPT_DIR/statusline.js")

# Try to inject git branch before ctx
BRANCH=""
if git rev-parse --git-dir > /dev/null 2>&1; then
    BRANCH=$(git branch --show-current 2>/dev/null)
fi

if [ -n "$BRANCH" ]; then
    echo "${RESULT/ | ctx:/ | $BRANCH | ctx:}"
else
    echo "$RESULT"
fi
