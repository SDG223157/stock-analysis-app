#!/bin/bash

# Check if tickers.ts exists
if [ ! -f "tickers.ts" ]; then
    echo "Error: tickers.ts file not found"
    exit 1
fi

# Create directory if it doesn't exist
mkdir -p app/utils

# Create the Python file with the correct format
cat << 'PYTHON_CONTENT' > app/utils/tickers.py
# Auto-generated from tickers.ts
TICKERS = [
PYTHON_CONTENT

# Extract and format the tickers
sed -n '/export const tickers = \[/,/\];/p' tickers.ts | \
    grep '{' | \
    grep 'symbol' | \
    sed 's/{ symbol: /{"symbol": /g' | \
    sed 's/, name: /, "name": /g' | \
    sed 's/},*/},/g' | \
    sed 's/^[[:space:]]*/    /' | \
    sed '$s/,$//' >> app/utils/tickers.py

# Add the closing content
cat << 'PYTHON_END' >> app/utils/tickers.py
]

# Create a dictionary for faster lookups
TICKER_DICT = {item["symbol"]: item["name"] for item in TICKERS}
PYTHON_END

echo "Conversion completed. Checking syntax..."

# Verify Python syntax
python3 -c "from app.utils.tickers import TICKERS, TICKER_DICT" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "Conversion successful!"
    echo "Output file: app/utils/tickers.py"
else
    echo "Error: Invalid Python syntax in output file"
    exit 1
fi
