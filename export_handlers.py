"""
Export handlers for generating schedule outputs in various formats.
"""
import json
import csv
from io import StringIO
from typing import List, Dict
from models import Schedule
from scheduler import AutoScheduler
from utils import format_date, format_training_list


class JSONExporter:
    """Export schedule to JSON format."""

    @staticmethod
    def export(schedule: Schedule) -> str:
        """
        Export schedule to JSON string.

        Args:
            schedule: The schedule to export

        Returns:
            JSON string representation of the schedule
        """
        return json.dumps(schedule.to_dict(), indent=2)

    @staticmethod
    def export_to_file(schedule: Schedule, filename: str) -> None:
        """
        Export schedule to JSON file.

        Args:
            schedule: The schedule to export
            filename: Path to the output file
        """
        with open(filename, 'w') as f:
            f.write(JSONExporter.export(schedule))


class CSVExporter:
    """Export schedule to CSV format."""

    @staticmethod
    def export_employees(schedule: Schedule) -> str:
        """
        Export employee data to CSV string.

        Args:
            schedule: The schedule to export

        Returns:
            CSV string with employee data
        """
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(['ID', 'Name', 'Position', 'Rank', 'Training', 'Max Hours', 'Assigned Hours', 'Available Hours'])

        for emp in schedule.employees:
            writer.writerow([
                emp.id,
                emp.name,
                emp.position,
                emp.rank,
                format_training_list(emp.training),
                emp.max_hours,
                emp.current_hours,
                emp.available_hours()
            ])

        return output.getvalue()

    @staticmethod
    def export_tasks(schedule: Schedule) -> str:
        """
        Export task data to CSV string.

        Args:
            schedule: The schedule to export

        Returns:
            CSV string with task data
        """
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(['ID', 'Name', 'Duration (hrs)', 'Priority', 'Min Rank', 'Required Training', 'Assigned To', 'Status'])

        for task in schedule.tasks:
            writer.writerow([
                task.id,
                task.name,
                task.duration,
                task.priority,
                task.min_rank,
                format_training_list(task.required_training),
                task.assigned_employee.name if task.assigned_employee else 'Unassigned',
                'Assigned' if task.is_assigned() else 'Unassigned'
            ])

        return output.getvalue()

    @staticmethod
    def export_schedule(schedule: Schedule) -> str:
        """
        Export complete schedule to CSV string.

        Args:
            schedule: The schedule to export

        Returns:
            CSV string with complete schedule
        """
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(['Employee ID', 'Employee Name', 'Position', 'Rank', 'Task ID', 'Task Name', 'Duration (hrs)', 'Priority'])

        for emp in schedule.employees:
            tasks = schedule.get_employee_tasks(emp)
            if tasks:
                for task in tasks:
                    writer.writerow([
                        emp.id,
                        emp.name,
                        emp.position,
                        emp.rank,
                        task.id,
                        task.name,
                        task.duration,
                        task.priority
                    ])
            else:
                writer.writerow([
                    emp.id,
                    emp.name,
                    emp.position,
                    emp.rank,
                    'N/A',
                    'No tasks assigned',
                    0,
                    'N/A'
                ])

        return output.getvalue()

    @staticmethod
    def export_to_file(schedule: Schedule, filename: str, export_type: str = 'schedule') -> None:
        """
        Export schedule to CSV file.

        Args:
            schedule: The schedule to export
            filename: Path to the output file
            export_type: Type of export ('schedule', 'employees', or 'tasks')
        """
        if export_type == 'employees':
            content = CSVExporter.export_employees(schedule)
        elif export_type == 'tasks':
            content = CSVExporter.export_tasks(schedule)
        else:
            content = CSVExporter.export_schedule(schedule)

        with open(filename, 'w') as f:
            f.write(content)


class ReportGenerator:
    """Generate formatted text reports."""

    @staticmethod
    def generate_summary(schedule: Schedule, scheduler: AutoScheduler = None) -> str:
        """
        Generate a summary report of the schedule.

        Args:
            schedule: The schedule to report on
            scheduler: Optional scheduler with unassigned task info

        Returns:
            Formatted text report
        """
        lines = []
        lines.append("=" * 80)
        lines.append("SCHEDULE SUMMARY REPORT")
        lines.append("=" * 80)
        lines.append(f"Period: {format_date(schedule.period_start)} to {format_date(schedule.period_end)}")
        lines.append(f"Generated: {format_date(schedule.created_at)}")
        lines.append("")

        stats = schedule.get_statistics()
        lines.append("STATISTICS")
        lines.append("-" * 80)
        lines.append(f"Total Employees:     {stats['total_employees']}")
        lines.append(f"Total Tasks:         {stats['total_tasks']}")
        lines.append(f"Assigned Tasks:      {stats['assigned_tasks']}")
        lines.append(f"Unassigned Tasks:    {stats['unassigned_tasks']}")
        lines.append(f"Completion Rate:     {stats['completion_rate']}%")
        lines.append(f"Total Hours:         {stats['total_hours_scheduled']}")
        lines.append(f"Avg Hours/Employee:  {stats['average_hours_per_employee']}")
        lines.append(f"Valid Schedule:      {'Yes' if stats['is_valid'] else 'No'}")
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def generate_employee_report(schedule: Schedule, scheduler: AutoScheduler = None) -> str:
        """
        Generate a detailed employee workload report.

        Args:
            schedule: The schedule to report on
            scheduler: Optional scheduler for additional info

        Returns:
            Formatted text report
        """
        lines = []
        lines.append("=" * 80)
        lines.append("EMPLOYEE WORKLOAD REPORT")
        lines.append("=" * 80)
        lines.append("")

        if scheduler:
            workload_report = scheduler.get_employee_workload_report()
        else:
            workload_report = []
            for emp in schedule.employees:
                tasks = schedule.get_employee_tasks(emp)
                workload_report.append({
                    'employee_name': emp.name,
                    'position': emp.position,
                    'rank': emp.rank,
                    'assigned_hours': emp.current_hours,
                    'max_hours': emp.max_hours,
                    'available_hours': emp.available_hours(),
                    'utilization': round((emp.current_hours / emp.max_hours) * 100, 2) if emp.max_hours > 0 else 0,
                    'task_count': len(tasks),
                    'tasks': [{'name': t.name, 'duration': t.duration} for t in tasks]
                })

        for emp_data in workload_report:
            lines.append(f"Employee: {emp_data['employee_name']}")
            lines.append(f"Position: {emp_data['position']} (Rank {emp_data['rank']})")
            lines.append(f"Hours: {emp_data['assigned_hours']}/{emp_data['max_hours']} ({emp_data['utilization']}% utilized)")
            lines.append(f"Available: {emp_data['available_hours']} hours")
            lines.append(f"Tasks Assigned: {emp_data['task_count']}")

            if emp_data['tasks']:
                lines.append("  Tasks:")
                for task in emp_data['tasks']:
                    lines.append(f"    - {task['name']} ({task['duration']}h)")
            else:
                lines.append("  No tasks assigned")

            lines.append("-" * 80)

        return "\n".join(lines)

    @staticmethod
    def generate_task_report(schedule: Schedule, scheduler: AutoScheduler = None) -> str:
        """
        Generate a detailed task assignment report.

        Args:
            schedule: The schedule to report on
            scheduler: Optional scheduler with unassigned task info

        Returns:
            Formatted text report
        """
        lines = []
        lines.append("=" * 80)
        lines.append("TASK ASSIGNMENT REPORT")
        lines.append("=" * 80)
        lines.append("")

        lines.append("ASSIGNED TASKS")
        lines.append("-" * 80)
        for task in schedule.get_assigned_tasks():
            lines.append(f"Task: {task.name} (ID: {task.id})")
            lines.append(f"  Duration: {task.duration}h | Priority: {task.priority}/10 | Min Rank: {task.min_rank}")
            lines.append(f"  Required Training: {format_training_list(task.required_training)}")
            lines.append(f"  Assigned To: {task.assigned_employee.name} ({task.assigned_employee.position})")
            lines.append("")

        if schedule.get_unassigned_tasks():
            lines.append("")
            lines.append("UNASSIGNED TASKS")
            lines.append("-" * 80)

            if scheduler:
                unassigned_report = scheduler.get_unassigned_tasks_report()
                for task_data in unassigned_report:
                    lines.append(f"Task: {task_data['task_name']} (ID: {task_data['task_id']})")
                    lines.append(f"  Duration: {task_data['duration']}h | Priority: {task_data['priority']}/10 | Min Rank: {task_data['min_rank']}")
                    lines.append(f"  Required Training: {', '.join(task_data['required_training'])}")
                    lines.append(f"  Reasons for non-assignment:")
                    for reason in task_data['reasons']:
                        lines.append(f"    - {reason}")
                    lines.append("")
            else:
                for task in schedule.get_unassigned_tasks():
                    lines.append(f"Task: {task.name} (ID: {task.id})")
                    lines.append(f"  Duration: {task.duration}h | Priority: {task.priority}/10 | Min Rank: {task.min_rank}")
                    lines.append(f"  Required Training: {format_training_list(task.required_training)}")
                    lines.append("")

        return "\n".join(lines)

    @staticmethod
    def generate_full_report(schedule: Schedule, scheduler: AutoScheduler = None) -> str:
        """
        Generate a complete report with all information.

        Args:
            schedule: The schedule to report on
            scheduler: Optional scheduler with additional info

        Returns:
            Formatted text report
        """
        return "\n\n".join([
            ReportGenerator.generate_summary(schedule, scheduler),
            ReportGenerator.generate_employee_report(schedule, scheduler),
            ReportGenerator.generate_task_report(schedule, scheduler)
        ])

    @staticmethod
    def export_to_file(schedule: Schedule, filename: str, scheduler: AutoScheduler = None, report_type: str = 'full') -> None:
        """
        Export report to text file.

        Args:
            schedule: The schedule to report on
            filename: Path to the output file
            scheduler: Optional scheduler with additional info
            report_type: Type of report ('full', 'summary', 'employees', or 'tasks')
        """
        if report_type == 'summary':
            content = ReportGenerator.generate_summary(schedule, scheduler)
        elif report_type == 'employees':
            content = ReportGenerator.generate_employee_report(schedule, scheduler)
        elif report_type == 'tasks':
            content = ReportGenerator.generate_task_report(schedule, scheduler)
        else:
            content = ReportGenerator.generate_full_report(schedule, scheduler)

        with open(filename, 'w') as f:
            f.write(content)
