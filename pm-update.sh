#!/bin/bash
# Usage: bash pm-update.sh <key> <state>
#   bash pm-update.sh pm running
#   bash pm-update.sh reset        — reset all to pending

KEY="$1"
STATE="$2"
PM_FILE="$HOME/.claude/pm-last.txt"

if [ -z "$KEY" ]; then
  echo "Usage: pm-update.sh <pm|sync|bye> <pending|running|done>" >&2
  echo "       pm-update.sh reset" >&2
  exit 1
fi

# Reset command
if [ "$KEY" = "reset" ]; then
  echo "pm:pending,sync:pending,bye:pending" > "$PM_FILE"
  exit 0
fi

# Read current state or initialize
CURRENT=""
if [ -f "$PM_FILE" ]; then
  CURRENT=$(cat "$PM_FILE" | tr -d '\r\n')
fi

if [ -z "$CURRENT" ]; then
  CURRENT="pm:pending,sync:pending,bye:pending"
fi

# Update the specific key
UPDATED=$(echo "$CURRENT" | sed "s/${KEY}:[a-z]*/${KEY}:${STATE}/")

echo "$UPDATED" > "$PM_FILE"
