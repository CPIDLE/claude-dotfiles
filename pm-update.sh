#!/bin/bash
# Usage: bash pm-update.sh <key> <state>
# Example: bash pm-update.sh pm running
# Updates ~/.claude/pm-last.txt with today's date and the given key:state

KEY="$1"
STATE="$2"
PM_FILE="$HOME/.claude/pm-last.txt"
TODAY=$(date +%Y-%m-%d)

if [ -z "$KEY" ] || [ -z "$STATE" ]; then
  echo "Usage: pm-update.sh <pm|sync|bye> <pending|running|done>" >&2
  exit 1
fi

# Read current state or initialize
CURRENT=""
if [ -f "$PM_FILE" ]; then
  FILE_DATE=$(cut -f1 "$PM_FILE")
  if [ "$FILE_DATE" = "$TODAY" ]; then
    CURRENT=$(cut -f2 "$PM_FILE")
  fi
fi

if [ -z "$CURRENT" ]; then
  CURRENT="pm:pending,sync:pending,bye:pending"
fi

# Update the specific key
UPDATED=$(echo "$CURRENT" | sed "s/${KEY}:[a-z]*/${KEY}:${STATE}/")

# Write back
printf '%s\t%s\n' "$TODAY" "$UPDATED" > "$PM_FILE"
