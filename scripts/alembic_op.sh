#!/bin/bash
# ----------------------------------------------------
# Purpose: Wrapper script to execute Alembic commands for the database_service
#          It ensures the correct environment (PYTHONPATH) and config file path
#          are used, enabling imports in alembic/env.py.
#
# Usage: ./scripts/alembic_op.sh revision --autogenerate -m "added users table"
#        ./scripts/alembic_op.sh upgrade head
# ----------------------------------------------------

# Exit immediately if a command exits with a non-zero status.
set -e

# Define the absolute path to the project root
PROJECT_ROOT=$(pwd)

# 1. Check for required arguments
if [ "$#" -eq 0 ]; then
    echo "Error: No Alembic command provided."
    echo "Usage: $0 [alembic command] [arguments...]"
    exit 1
fi

# 2. Set the PYTHONPATH environment variable
export PYTHONPATH="$PROJECT_ROOT"

# 3. Define the service-specific configuration file path
ALEMBIC_CONFIG_PATH="database_service/alembic.ini"


echo "PYTHONPATH set to: $PYTHONPATH"

# 4. Execute the Alembic command using Poetry

poetry run --directory database_service alembic \
    -c "$PROJECT_ROOT/$ALEMBIC_CONFIG_PATH" \
    "$@"
