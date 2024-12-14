#!/bin/bash

# Create necessary directories
mkdir -p app/utils
mkdir -p scripts

# Copy the conversion script and make it executable
cp scripts/convert_tickers.py scripts/
chmod +x scripts/convert_tickers.py

# Run the conversion script if tickers.ts exists
if [ -f "tickers.ts" ]; then
    python3 scripts/convert_tickers.py
else
    # If tickers.ts doesn't exist, use the default tickers.py
    mkdir -p app/utils
    cp tickers.py app/utils/
fi

# Install required packages if not already installed
pip install -r requirements.txt

echo "Setup completed successfully!"
