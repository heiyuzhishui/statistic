#!/bin/bash

# Process JSON files and extract coordinates names
echo "Processing JSON files..."
find . -type f -name "*.json" -print0 | xargs -0 cat | jq -r '.region[]?.coordinates.name' | sort | uniq -c | sort -rn | awk '{printf "%s\t%s\n", $1, $2}'

echo "---------------------------------"

# Process XML files and extract <name> tags
echo "Processing XML files..."
find . -type f -name "*.xml" -print0 | xargs -0 grep -hR "<name>" | cut -d '>' -f 2 | cut -d '<' -f 1 | sort | uniq -c | sort -nr
