#!/bin/bash

echo "Running ruff check on _config.py..."
ruff check httpx/_config.py

echo -e "\nRunning ruff check on _transports/default.py..."
ruff check httpx/_transports/default.py

echo -e "\nChecking if issues can be fixed automatically..."
ruff check --diff --fix httpx/_config.py httpx/_transports/default.py