#!/usr/bin/env python3
"""
Demo script for the Automatic Scheduling System.
Shows how the system works with sample data.
"""
from datetime import datetime
from models import Employee, Task, Schedule
from scheduler import AutoScheduler
from export_handlers import ReportGenerator
from utils import get_current_two_week_period

print("=" * 80)
print("  AUTOMATIC SCHEDULING SYSTEM - DEMO")
print("=" * 80)
print()

# Create sample employees
print("Creating sample employees...")
employees = [
    Employee(
        id=1,
        name="Alice Johnson",
        training={"Python", "JavaScript", "Database", "Leadership"},
        rank=8,
        position="Senior Software Engineer",
        max_hours=80
    ),
    Employee(
        id=2,
        name="Bob Smith",
        training={"Python", "Database", "Testing"},
        rank=5,
        position="Software Engineer",
        max_hours=80
    ),
    Employee(
        id=3,
        name="Carol Williams",
        training={"JavaScript", "HTML", "CSS", "Design"},
        rank=6,
        position="Frontend Developer",
        max_hours=60
    ),
    Employee(
        id=4,
        name="David Brown",
        training={"Python", "Machine Learning", "Database"},
        rank=7,
        position="Data Scientist",
        max_hours=70
    ),
]

for emp in employees:
    print(f"  ✓ {emp.name} ({emp.position}, Rank {emp.rank})")

print()

# Create sample tasks
print("Creating sample tasks...")
tasks = [
    Task(
        id=1,
        name="Build User Authentication API",
        required_training={"Python", "Database"},
        duration=20,
        priority=9,
        min_rank=5
    ),
    Task(
        id=2,
        name="Design Dashboard UI",
        required_training={"JavaScript", "HTML", "CSS"},
        duration=15,
        priority=8,
        min_rank=4
    ),
    Task(
        id=3,
        name="Implement Data Pipeline",
        required_training={"Python", "Database"},
        duration=25,
        priority=10,
        min_rank=6
    ),
    Task(
        id=4,
        name="Write Unit Tests",
        required_training={"Python", "Testing"},
        duration=12,
        priority=7,
        min_rank=4
    ),
    Task(
        id=5,
        name="Deploy ML Model",
        required_training={"Python", "Machine Learning"},
        duration=18,
        priority=9,
        min_rank=7
    ),
    Task(
        id=6,
        name="Code Review Process",
        required_training={"Leadership", "Python"},
        duration=10,
        priority=6,
        min_rank=7
    ),
]

for task in tasks:
    print(f"  ✓ {task.name} (Priority {task.priority}/10, {task.duration}h)")

print()

# Create schedule
print("Generating schedule for 2-week period...")
period_start, period_end = get_current_two_week_period()
schedule = Schedule(
    employees=employees,
    tasks=tasks,
    period_start=period_start,
    period_end=period_end
)

# Run scheduler
scheduler = AutoScheduler(schedule)
success = scheduler.schedule_all()

stats = schedule.get_statistics()

print(f"Period: {period_start.strftime('%Y-%m-%d')} to {period_end.strftime('%Y-%m-%d')}")
print(f"✓ Schedule generated!")
print()
print(f"Results:")
print(f"  - Total Tasks: {stats['total_tasks']}")
print(f"  - Assigned: {stats['assigned_tasks']}")
print(f"  - Unassigned: {stats['unassigned_tasks']}")
print(f"  - Completion Rate: {stats['completion_rate']}%")
print()

# Display full report
print("=" * 80)
print(ReportGenerator.generate_full_report(schedule, scheduler))

# Export files
print()
print("=" * 80)
print("Exporting schedule to files...")
print("=" * 80)

from export_handlers import JSONExporter, CSVExporter

# Export JSON
JSONExporter.export_to_file(schedule, "demo_schedule.json")
print("✓ Exported JSON: demo_schedule.json")

# Export CSV
CSVExporter.export_to_file(schedule, "demo_schedule.csv", 'schedule')
print("✓ Exported CSV (schedule): demo_schedule.csv")

CSVExporter.export_to_file(schedule, "demo_employees.csv", 'employees')
print("✓ Exported CSV (employees): demo_employees.csv")

CSVExporter.export_to_file(schedule, "demo_tasks.csv", 'tasks')
print("✓ Exported CSV (tasks): demo_tasks.csv")

# Export text report
ReportGenerator.export_to_file(schedule, "demo_report.txt", scheduler, 'full')
print("✓ Exported text report: demo_report.txt")

print()
print("=" * 80)
print("Demo complete!")
print("=" * 80)
print()
print("Files created:")
print("  - demo_schedule.json (full schedule data)")
print("  - demo_schedule.csv (schedule assignments)")
print("  - demo_employees.csv (employee data)")
print("  - demo_tasks.csv (task data)")
print("  - demo_report.txt (full text report)")
print()
print("You can:")
print("  1. View the report: cat demo_report.txt")
print("  2. Check the JSON: cat demo_schedule.json")
print("  3. Open CSVs in Excel or any spreadsheet app")
print()
print("To use the interactive CLI in your own terminal:")
print("  python scheduler_cli.py")
print()
