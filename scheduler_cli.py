#!/usr/bin/env python3
"""
Command-line interface for the Automatic Scheduling System.
"""
import sys
from datetime import datetime
from models import Employee, Task, Schedule
from scheduler import AutoScheduler
from export_handlers import JSONExporter, CSVExporter, ReportGenerator
from utils import get_current_two_week_period, parse_training_list, format_training_list


class SchedulerCLI:
    def __init__(self):
        self.employees = []
        self.tasks = []
        self.next_emp_id = 1
        self.next_task_id = 1
        self.schedule = None
        self.scheduler = None

    def show_menu(self):
        """Display main menu."""
        print("\n" + "=" * 60)
        print("  AUTOMATIC SCHEDULING SYSTEM - CLI")
        print("=" * 60)
        print("\n[1] Manage Employees")
        print("[2] Manage Tasks")
        print("[3] Generate Schedule")
        print("[4] View Schedule")
        print("[5] Export Schedule")
        print("[6] View Statistics")
        print("[0] Exit")
        print("\n" + "-" * 60)

    def employee_menu(self):
        """Employee management menu."""
        while True:
            print("\n" + "=" * 60)
            print("  EMPLOYEE MANAGEMENT")
            print("=" * 60)
            print("\n[1] Add Employee")
            print("[2] View All Employees")
            print("[3] Delete Employee")
            print("[0] Back to Main Menu")
            print("\n" + "-" * 60)

            choice = input("Select option: ").strip()

            if choice == "1":
                self.add_employee()
            elif choice == "2":
                self.view_employees()
            elif choice == "3":
                self.delete_employee()
            elif choice == "0":
                break
            else:
                print("Invalid option!")

    def add_employee(self):
        """Add a new employee interactively."""
        print("\n--- Add New Employee ---")

        name = input("Name: ").strip()
        if not name:
            print("Error: Name cannot be empty!")
            return

        position = input("Position (e.g., Software Engineer): ").strip()
        if not position:
            print("Error: Position cannot be empty!")
            return

        try:
            rank = int(input("Rank (1-10, where 10 is most senior): ").strip())
            if rank < 1 or rank > 10:
                print("Error: Rank must be between 1 and 10!")
                return
        except ValueError:
            print("Error: Rank must be a number!")
            return

        try:
            max_hours = float(input("Max hours for 2-week period (e.g., 80): ").strip())
            if max_hours <= 0:
                print("Error: Hours must be positive!")
                return
        except ValueError:
            print("Error: Hours must be a number!")
            return

        training_str = input("Training/Skills (comma-separated, e.g., Python,JavaScript,Database): ").strip()
        training = parse_training_list(training_str)
        if not training:
            print("Error: At least one skill is required!")
            return

        employee = Employee(
            id=self.next_emp_id,
            name=name,
            training=training,
            rank=rank,
            position=position,
            max_hours=max_hours
        )

        self.employees.append(employee)
        self.next_emp_id += 1
        print(f"\n✓ Employee '{name}' added successfully! (ID: {employee.id})")

    def view_employees(self):
        """Display all employees."""
        if not self.employees:
            print("\nNo employees added yet.")
            return

        print("\n" + "=" * 80)
        print("  ALL EMPLOYEES")
        print("=" * 80)
        print(f"\n{'ID':<5} {'Name':<20} {'Position':<20} {'Rank':<6} {'Hours':<12} {'Skills'}")
        print("-" * 80)

        for emp in self.employees:
            hours_info = f"{emp.current_hours}/{emp.max_hours}"
            skills = format_training_list(emp.training)
            print(f"{emp.id:<5} {emp.name:<20} {emp.position:<20} {emp.rank:<6} {hours_info:<12} {skills}")

    def delete_employee(self):
        """Delete an employee by ID."""
        if not self.employees:
            print("\nNo employees to delete.")
            return

        self.view_employees()
        try:
            emp_id = int(input("\nEnter Employee ID to delete (0 to cancel): ").strip())
            if emp_id == 0:
                return

            employee = next((e for e in self.employees if e.id == emp_id), None)
            if employee:
                confirm = input(f"Delete '{employee.name}'? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    self.employees.remove(employee)
                    print(f"\n✓ Employee '{employee.name}' deleted.")
                else:
                    print("Cancelled.")
            else:
                print(f"Error: Employee ID {emp_id} not found!")
        except ValueError:
            print("Error: Invalid ID!")

    def task_menu(self):
        """Task management menu."""
        while True:
            print("\n" + "=" * 60)
            print("  TASK MANAGEMENT")
            print("=" * 60)
            print("\n[1] Add Task")
            print("[2] View All Tasks")
            print("[3] Delete Task")
            print("[0] Back to Main Menu")
            print("\n" + "-" * 60)

            choice = input("Select option: ").strip()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.delete_task()
            elif choice == "0":
                break
            else:
                print("Invalid option!")

    def add_task(self):
        """Add a new task interactively."""
        print("\n--- Add New Task ---")

        name = input("Task name: ").strip()
        if not name:
            print("Error: Task name cannot be empty!")
            return

        try:
            duration = float(input("Duration in hours (e.g., 8): ").strip())
            if duration <= 0:
                print("Error: Duration must be positive!")
                return
        except ValueError:
            print("Error: Duration must be a number!")
            return

        try:
            priority = int(input("Priority (1-10, where 10 is highest): ").strip())
            if priority < 1 or priority > 10:
                print("Error: Priority must be between 1 and 10!")
                return
        except ValueError:
            print("Error: Priority must be a number!")
            return

        try:
            min_rank = int(input("Minimum rank required (1-10): ").strip())
            if min_rank < 1 or min_rank > 10:
                print("Error: Minimum rank must be between 1 and 10!")
                return
        except ValueError:
            print("Error: Minimum rank must be a number!")
            return

        training_str = input("Required skills (comma-separated, e.g., Python,Database): ").strip()
        required_training = parse_training_list(training_str)
        if not required_training:
            print("Error: At least one required skill is needed!")
            return

        task = Task(
            id=self.next_task_id,
            name=name,
            required_training=required_training,
            duration=duration,
            priority=priority,
            min_rank=min_rank
        )

        self.tasks.append(task)
        self.next_task_id += 1
        print(f"\n✓ Task '{name}' added successfully! (ID: {task.id})")

    def view_tasks(self):
        """Display all tasks."""
        if not self.tasks:
            print("\nNo tasks added yet.")
            return

        print("\n" + "=" * 100)
        print("  ALL TASKS")
        print("=" * 100)
        print(f"\n{'ID':<5} {'Name':<25} {'Duration':<10} {'Priority':<10} {'Min Rank':<10} {'Assigned To':<20}")
        print("-" * 100)

        for task in self.tasks:
            assigned = task.assigned_employee.name if task.assigned_employee else "Unassigned"
            print(f"{task.id:<5} {task.name:<25} {task.duration}h{'':<7} {task.priority}/10{'':<6} {task.min_rank}{'':<9} {assigned:<20}")

    def delete_task(self):
        """Delete a task by ID."""
        if not self.tasks:
            print("\nNo tasks to delete.")
            return

        self.view_tasks()
        try:
            task_id = int(input("\nEnter Task ID to delete (0 to cancel): ").strip())
            if task_id == 0:
                return

            task = next((t for t in self.tasks if t.id == task_id), None)
            if task:
                confirm = input(f"Delete '{task.name}'? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    self.tasks.remove(task)
                    print(f"\n✓ Task '{task.name}' deleted.")
                else:
                    print("Cancelled.")
            else:
                print(f"Error: Task ID {task_id} not found!")
        except ValueError:
            print("Error: Invalid ID!")

    def generate_schedule(self):
        """Generate the schedule using the scheduler algorithm."""
        if not self.employees:
            print("\nError: No employees available! Add employees first.")
            return

        if not self.tasks:
            print("\nError: No tasks available! Add tasks first.")
            return

        print("\n" + "=" * 60)
        print("  GENERATING SCHEDULE...")
        print("=" * 60)

        period_start, period_end = get_current_two_week_period()
        self.schedule = Schedule(
            employees=self.employees,
            tasks=self.tasks,
            period_start=period_start,
            period_end=period_end
        )

        self.scheduler = AutoScheduler(self.schedule)
        success = self.scheduler.schedule_all()

        stats = self.schedule.get_statistics()

        print(f"\n✓ Schedule generated!")
        print(f"\nPeriod: {period_start.strftime('%Y-%m-%d')} to {period_end.strftime('%Y-%m-%d')}")
        print(f"Total tasks: {stats['total_tasks']}")
        print(f"Assigned: {stats['assigned_tasks']}")
        print(f"Unassigned: {stats['unassigned_tasks']}")
        print(f"Completion rate: {stats['completion_rate']}%")

        if not success:
            print(f"\n⚠ Warning: {stats['unassigned_tasks']} task(s) could not be assigned.")
            print("Use 'View Schedule' to see details.")

    def view_schedule(self):
        """View the generated schedule."""
        if not self.schedule:
            print("\nNo schedule generated yet. Generate a schedule first!")
            return

        while True:
            print("\n" + "=" * 60)
            print("  VIEW SCHEDULE")
            print("=" * 60)
            print("\n[1] Summary Report")
            print("[2] Employee Workload Report")
            print("[3] Task Assignment Report")
            print("[4] Full Report")
            print("[0] Back to Main Menu")
            print("\n" + "-" * 60)

            choice = input("Select option: ").strip()

            if choice == "1":
                print("\n" + ReportGenerator.generate_summary(self.schedule, self.scheduler))
            elif choice == "2":
                print("\n" + ReportGenerator.generate_employee_report(self.schedule, self.scheduler))
            elif choice == "3":
                print("\n" + ReportGenerator.generate_task_report(self.schedule, self.scheduler))
            elif choice == "4":
                print("\n" + ReportGenerator.generate_full_report(self.schedule, self.scheduler))
            elif choice == "0":
                break
            else:
                print("Invalid option!")

    def export_schedule(self):
        """Export schedule to files."""
        if not self.schedule:
            print("\nNo schedule generated yet. Generate a schedule first!")
            return

        print("\n" + "=" * 60)
        print("  EXPORT SCHEDULE")
        print("=" * 60)
        print("\n[1] Export as JSON")
        print("[2] Export as CSV (Complete Schedule)")
        print("[3] Export as CSV (Employees)")
        print("[4] Export as CSV (Tasks)")
        print("[5] Export as Text Report")
        print("[0] Back to Main Menu")
        print("\n" + "-" * 60)

        choice = input("Select option: ").strip()

        if choice == "1":
            filename = "schedule_export.json"
            JSONExporter.export_to_file(self.schedule, filename)
            print(f"\n✓ Exported to {filename}")

        elif choice == "2":
            filename = "schedule_export.csv"
            CSVExporter.export_to_file(self.schedule, filename, 'schedule')
            print(f"\n✓ Exported to {filename}")

        elif choice == "3":
            filename = "employees_export.csv"
            CSVExporter.export_to_file(self.schedule, filename, 'employees')
            print(f"\n✓ Exported to {filename}")

        elif choice == "4":
            filename = "tasks_export.csv"
            CSVExporter.export_to_file(self.schedule, filename, 'tasks')
            print(f"\n✓ Exported to {filename}")

        elif choice == "5":
            filename = "schedule_report.txt"
            ReportGenerator.export_to_file(self.schedule, filename, self.scheduler, 'full')
            print(f"\n✓ Exported to {filename}")

        elif choice == "0":
            return
        else:
            print("Invalid option!")

    def view_statistics(self):
        """View schedule statistics."""
        if not self.schedule:
            print("\nNo schedule generated yet. Generate a schedule first!")
            return

        stats = self.schedule.get_statistics()

        print("\n" + "=" * 60)
        print("  SCHEDULE STATISTICS")
        print("=" * 60)
        print(f"\nTotal Employees:       {stats['total_employees']}")
        print(f"Total Tasks:           {stats['total_tasks']}")
        print(f"Assigned Tasks:        {stats['assigned_tasks']}")
        print(f"Unassigned Tasks:      {stats['unassigned_tasks']}")
        print(f"Completion Rate:       {stats['completion_rate']}%")
        print(f"Total Hours Scheduled: {stats['total_hours_scheduled']}")
        print(f"Avg Hours/Employee:    {stats['average_hours_per_employee']}")
        print(f"Valid Schedule:        {'Yes' if stats['is_valid'] else 'No'}")

    def run(self):
        """Main CLI loop."""
        print("\n" + "=" * 60)
        print("  Welcome to the Automatic Scheduling System!")
        print("=" * 60)

        while True:
            self.show_menu()
            choice = input("Select option: ").strip()

            if choice == "1":
                self.employee_menu()
            elif choice == "2":
                self.task_menu()
            elif choice == "3":
                self.generate_schedule()
            elif choice == "4":
                self.view_schedule()
            elif choice == "5":
                self.export_schedule()
            elif choice == "6":
                self.view_statistics()
            elif choice == "0":
                print("\nThank you for using the Automatic Scheduling System!")
                print("Goodbye!\n")
                sys.exit(0)
            else:
                print("\nInvalid option! Please try again.")


if __name__ == "__main__":
    cli = SchedulerCLI()
    cli.run()
