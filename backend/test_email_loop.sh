#!/bin/bash
# Script to run email reminders in a loop for testing
# Usage: ./test_email_loop.sh [interval_in_seconds]
# Default: 5 seconds

INTERVAL=${1:-5}

echo "Running email reminders every ${INTERVAL} seconds..."
echo "Press Ctrl+C to stop"
echo ""

while true; do
    echo "============================================================"
    echo "$(date): Running email reminder script..."
    echo "============================================================"
    python3 send_email_reminders.py
    echo ""
    echo "Waiting ${INTERVAL} seconds before next run..."
    echo ""
    sleep $INTERVAL
done

