#!/bin/bash
# Source this file to add itsup to your PATH
# Usage: source env.sh

# Get the directory where this script lives
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"

# Activate virtual environment
if [ -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
    echo "✓ Activated Python virtual environment"
else
    echo "⚠ Virtual environment not found. Run 'make install' first."
    return 1
fi
