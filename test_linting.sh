#!/bin/bash

# Run the linting check on the problematic files
echo "Running ruff check on httpx/_config.py"
ruff check httpx/_config.py

echo "Running ruff check on httpx/_transports/default.py"
ruff check httpx/_transports/default.py

# Exit with the same code as the last command
exit $?