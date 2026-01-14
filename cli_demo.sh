#!/bin/bash
# Command-line interface for the Auto Scheduler

BASE_URL="http://127.0.0.1:5000"

echo "=== Auto Scheduler CLI ==="
echo ""

# Add employee example
add_employee() {
    echo "Adding employee..."
    curl -X POST "${BASE_URL}/employees/add" \
        -d "name=John Smith" \
        -d "position=Software Engineer" \
        -d "rank=7" \
        -d "max_hours=80" \
        -d "training=Python,JavaScript,Database" \
        -L -s > /dev/null
    echo "✓ Employee added"
}

# Add task example
add_task() {
    echo "Adding task..."
    curl -X POST "${BASE_URL}/tasks/add" \
        -d "name=Build API" \
        -d "duration=20" \
        -d "priority=8" \
        -d "min_rank=5" \
        -d "required_training=Python,Database" \
        -L -s > /dev/null
    echo "✓ Task added"
}

# Generate schedule
generate_schedule() {
    echo "Generating schedule..."
    curl -X POST "${BASE_URL}/schedule/generate" -L -s > /dev/null
    echo "✓ Schedule generated"
}

# Export schedule as JSON
export_json() {
    echo "Exporting schedule to schedule.json..."
    curl "${BASE_URL}/export/json" -o schedule.json -s
    echo "✓ Exported to schedule.json"
}

# Export report
export_report() {
    echo "Exporting full report to report.txt..."
    curl "${BASE_URL}/export/report/full" -o report.txt -s
    echo "✓ Exported to report.txt"
}

# Run demo
echo "Running demo with sample data..."
echo ""
add_employee
add_task
generate_schedule
export_json
export_report
echo ""
echo "=== Demo Complete ==="
echo "Files created:"
echo "  - schedule.json (JSON export)"
echo "  - report.txt (Full report)"
echo ""
echo "View the report:"
echo "  cat report.txt"
