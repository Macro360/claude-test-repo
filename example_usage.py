#!/usr/bin/env python3
"""
Example: Using the Automatic Scheduling System as a Python Library

This demonstrates how to integrate the scheduler into your own Python code.
"""

# Import the scheduling system components
from models import Employee, Task, Schedule
from scheduler import AutoScheduler
from export_handlers import JSONExporter, CSVExporter, ReportGenerator
from utils import get_current_two_week_period, parse_training_list
from datetime import datetime

# ============================================================================
# EXAMPLE 1: Basic Usage
# ============================================================================
print("=" * 70)
print("EXAMPLE 1: Basic Scheduling")
print("=" * 70)

# Step 1: Create employees
employees = [
    Employee(
        id=1,
        name="Sarah Chen",
        training={"Python", "Docker", "Kubernetes"},
        rank=9,
        position="DevOps Engineer",
        max_hours=80
    ),
    Employee(
        id=2,
        name="Mike Johnson",
        training={"Python", "Django", "PostgreSQL"},
        rank=6,
        position="Backend Developer",
        max_hours=80
    )
]

# Step 2: Create tasks
tasks = [
    Task(
        id=1,
        name="Deploy to Production",
        required_training={"Docker", "Kubernetes"},
        duration=15,
        priority=10,
        min_rank=7
    ),
    Task(
        id=2,
        name="Build REST API",
        required_training={"Python", "Django"},
        duration=30,
        priority=8,
        min_rank=5
    )
]

# Step 3: Create schedule for 2-week period
period_start, period_end = get_current_two_week_period()
schedule = Schedule(
    employees=employees,
    tasks=tasks,
    period_start=period_start,
    period_end=period_end
)

# Step 4: Run the scheduler
scheduler = AutoScheduler(schedule)
success = scheduler.schedule_all()

# Step 5: Check results
stats = schedule.get_statistics()
print(f"\n✓ Schedule generated!")
print(f"  Assigned: {stats['assigned_tasks']}/{stats['total_tasks']} tasks")
print(f"  Completion: {stats['completion_rate']}%")

# Step 6: View assignments
print("\nAssignments:")
for task in schedule.get_assigned_tasks():
    print(f"  - {task.name} → {task.assigned_employee.name}")

print("\n")

# ============================================================================
# EXAMPLE 2: Handling Unassigned Tasks
# ============================================================================
print("=" * 70)
print("EXAMPLE 2: Dealing with Unassigned Tasks")
print("=" * 70)

# Create a task that can't be assigned (requires skills nobody has)
impossible_task = Task(
    id=3,
    name="Machine Learning Model",
    required_training={"Machine Learning", "TensorFlow"},  # Nobody has these
    duration=40,
    priority=9,
    min_rank=7
)

schedule.tasks.append(impossible_task)

# Reset and regenerate
schedule.reset()
scheduler = AutoScheduler(schedule)
scheduler.schedule_all()

# Check for unassigned tasks
unassigned = scheduler.get_unassigned_tasks_report()
if unassigned:
    print(f"\n⚠ Warning: {len(unassigned)} task(s) could not be assigned\n")
    for task_info in unassigned:
        print(f"Task: {task_info['task_name']}")
        print(f"  Reasons:")
        for reason in task_info['reasons']:
            print(f"    - {reason}")

print("\n")

# ============================================================================
# EXAMPLE 3: Employee Workload Analysis
# ============================================================================
print("=" * 70)
print("EXAMPLE 3: Analyzing Employee Workload")
print("=" * 70)

workload = scheduler.get_employee_workload_report()
print("\nEmployee Workload:")
for emp_data in workload:
    print(f"\n{emp_data['employee_name']}:")
    print(f"  Hours: {emp_data['assigned_hours']}/{emp_data['max_hours']}")
    print(f"  Utilization: {emp_data['utilization']}%")
    print(f"  Tasks: {emp_data['task_count']}")
    if emp_data['tasks']:
        for task in emp_data['tasks']:
            print(f"    - {task['name']} ({task['duration']}h)")

print("\n")

# ============================================================================
# EXAMPLE 4: Programmatic Export
# ============================================================================
print("=" * 70)
print("EXAMPLE 4: Exporting Data Programmatically")
print("=" * 70)

# Export to JSON
json_data = JSONExporter.export(schedule)
print(f"\nJSON export (first 200 chars):")
print(json_data[:200] + "...")

# Export to CSV (as string)
csv_data = CSVExporter.export_schedule(schedule)
print(f"\nCSV export (first 3 lines):")
print('\n'.join(csv_data.split('\n')[:3]))

# Generate text report
report = ReportGenerator.generate_summary(schedule, scheduler)
print(f"\nText report (first 5 lines):")
print('\n'.join(report.split('\n')[:5]))

print("\n")

# ============================================================================
# EXAMPLE 5: Dynamic Skill Parsing
# ============================================================================
print("=" * 70)
print("EXAMPLE 5: Creating Employees from User Input")
print("=" * 70)

# Simulate getting data from user input, config file, or API
employee_data = {
    'name': 'Emily Rodriguez',
    'position': 'Full Stack Developer',
    'rank': 7,
    'max_hours': 75,
    'skills': 'React, Node.js, MongoDB, AWS'  # Comma-separated string
}

# Parse the skills string into a set
skills = parse_training_list(employee_data['skills'])

# Create employee
new_employee = Employee(
    id=3,
    name=employee_data['name'],
    training=skills,
    rank=employee_data['rank'],
    position=employee_data['position'],
    max_hours=employee_data['max_hours']
)

print(f"\nCreated employee: {new_employee.name}")
print(f"  Skills: {', '.join(sorted(new_employee.training))}")
print(f"  Available hours: {new_employee.available_hours()}")

print("\n")

# ============================================================================
# EXAMPLE 6: Custom Date Ranges
# ============================================================================
print("=" * 70)
print("EXAMPLE 6: Custom Scheduling Periods")
print("=" * 70)

from datetime import timedelta
from utils import get_two_week_period

# Schedule for a specific future period
future_start = datetime(2026, 2, 1)
period_start, period_end = get_two_week_period(future_start)

custom_schedule = Schedule(
    employees=[employees[0]],  # Just Sarah
    tasks=[tasks[0]],          # Just the deployment task
    period_start=period_start,
    period_end=period_end
)

print(f"\nCustom period: {period_start.strftime('%Y-%m-%d')} to {period_end.strftime('%Y-%m-%d')}")
print(f"Employees: {len(custom_schedule.employees)}")
print(f"Tasks: {len(custom_schedule.tasks)}")

print("\n")

# ============================================================================
# EXAMPLE 7: Checking Schedule Validity
# ============================================================================
print("=" * 70)
print("EXAMPLE 7: Schedule Validation")
print("=" * 70)

# Create a valid schedule
valid_schedule = Schedule(
    employees=[employees[0]],
    tasks=[tasks[0]],
    period_start=period_start,
    period_end=period_end
)

scheduler = AutoScheduler(valid_schedule)
scheduler.schedule_all()

print(f"\nSchedule is valid: {valid_schedule.is_valid()}")

# Now manually break it (assign too many hours)
employees[0].current_hours = 100  # Exceed max_hours of 80

print(f"After exceeding hours: {valid_schedule.is_valid()}")

# Reset
employees[0].reset_hours()
print(f"After reset: {valid_schedule.is_valid()}")

print("\n")

# ============================================================================
# EXAMPLE 8: Integration Pattern
# ============================================================================
print("=" * 70)
print("EXAMPLE 8: Integration with Your Application")
print("=" * 70)

def schedule_team(employee_list, task_list):
    """
    Function you can call from your own application.

    Args:
        employee_list: List of dicts with employee data
        task_list: List of dicts with task data

    Returns:
        dict with schedule results and statistics
    """
    # Convert dicts to Employee objects
    employees = []
    for i, emp_data in enumerate(employee_list, 1):
        employees.append(Employee(
            id=i,
            name=emp_data['name'],
            training=set(emp_data['skills']),
            rank=emp_data['rank'],
            position=emp_data['position'],
            max_hours=emp_data['max_hours']
        ))

    # Convert dicts to Task objects
    tasks = []
    for i, task_data in enumerate(task_list, 1):
        tasks.append(Task(
            id=i,
            name=task_data['name'],
            required_training=set(task_data['required_skills']),
            duration=task_data['duration'],
            priority=task_data['priority'],
            min_rank=task_data['min_rank']
        ))

    # Create and run scheduler
    period_start, period_end = get_current_two_week_period()
    schedule = Schedule(employees, tasks, period_start, period_end)
    scheduler = AutoScheduler(schedule)
    scheduler.schedule_all()

    # Return results
    return {
        'success': len(schedule.get_unassigned_tasks()) == 0,
        'statistics': schedule.get_statistics(),
        'assignments': [
            {
                'task': task.name,
                'employee': task.assigned_employee.name if task.assigned_employee else None,
                'duration': task.duration
            }
            for task in schedule.tasks
        ],
        'unassigned': scheduler.get_unassigned_tasks_report()
    }

# Example usage
my_employees = [
    {'name': 'Alice', 'skills': ['Python', 'AWS'], 'rank': 8, 'position': 'Cloud Architect', 'max_hours': 80},
    {'name': 'Bob', 'skills': ['Python', 'Django'], 'rank': 5, 'position': 'Developer', 'max_hours': 80}
]

my_tasks = [
    {'name': 'Setup AWS', 'required_skills': ['AWS'], 'duration': 20, 'priority': 9, 'min_rank': 7},
    {'name': 'Build API', 'required_skills': ['Python', 'Django'], 'duration': 30, 'priority': 8, 'min_rank': 5}
]

result = schedule_team(my_employees, my_tasks)

print(f"\nIntegration Example Results:")
print(f"  Success: {result['success']}")
print(f"  Completion: {result['statistics']['completion_rate']}%")
print(f"\n  Assignments:")
for assignment in result['assignments']:
    if assignment['employee']:
        print(f"    {assignment['task']} → {assignment['employee']} ({assignment['duration']}h)")

print("\n")
print("=" * 70)
print("Examples complete! You can adapt these patterns for your needs.")
print("=" * 70)
