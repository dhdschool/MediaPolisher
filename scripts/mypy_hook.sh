#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Extract unique service directories from the list of staged files ($@).
# 1. Echoes all files (e.g., api_gateway/main.py database_service/config.py)
# 2. Replaces spaces with newlines (tr ' ' '\n')
# 3. Extracts the first directory component (awk -F'/' '{print $1}')
# 4. Sorts and gets only unique directory names (sort | uniq)
SERVICE_DIRS=$(echo "$@" | tr ' ' '\n' | awk -F'/' '{print $1}' | sort | uniq)

EXIT_CODE=0

for SERVICE_DIR in $SERVICE_DIRS; do

    # Only proceed if the directory exists AND contains a pyproject.toml
    if [ -d "$SERVICE_DIR" ] && [ -f "$SERVICE_DIR/pyproject.toml" ]; then

        echo "--- Processing Service: $SERVICE_DIR ---"

        # 1. Change to the service directory (using the absolute path helps Mypy)
        # We save the current directory (project root) to return to it later
        CURRENT_DIR=$(pwd)
        cd "$SERVICE_DIR"

        # 2. Ensure the isolated environment is up to date based on poetry.lock
        poetry install --only main --no-root

        # 3. Find files belonging to THIS service (relative to the project root)
        # We filter the full list of staged files ($@) to only include those starting
        # with the current service directory name.
        SERVICE_FILES=$(echo "$@" | tr ' ' '\n' | grep "^$SERVICE_DIR/" | tr '\n' ' ')

        # 4. Run Mypy using the service's environment.
        # We use the root pyproject.toml (../pyproject.toml) for global config.
        # We pass only the filtered files.
        poetry run mypy --config-file ../pyproject.toml $SERVICE_FILES || EXIT_CODE=$?

        # 5. Return to the project root before checking the next service
        cd "$CURRENT_DIR"

    else
        echo "Skipping non-service directory: $SERVICE_DIR"
    fi
done

# The script must exit with the highest error code found during the loop
exit $EXIT_CODE
