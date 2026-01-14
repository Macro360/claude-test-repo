"""
Automatic scheduling engine with constraint satisfaction.
"""
from typing import List, Dict, Tuple
from models import Employee, Task, Schedule


class AutoScheduler:
    """
    Automatic scheduler that assigns tasks to employees based on constraints.

    The scheduler uses a greedy algorithm with the following strategy:
    1. Sort tasks by priority (high to low) and deadline
    2. For each task, find eligible employees
    3. Select the best employee based on a scoring system
    4. Assign the task to the selected employee
    """

    def __init__(self, schedule: Schedule):
        """
        Initialize the scheduler with a schedule.

        Args:
            schedule: The schedule to populate with assignments
        """
        self.schedule = schedule
        self.unassigned_reasons: Dict[int, List[str]] = {}

    def schedule_all(self) -> bool:
        """
        Schedule all tasks in the schedule.

        Returns:
            True if all tasks were assigned, False otherwise
        """
        self.schedule.reset()
        self.unassigned_reasons.clear()

        sorted_tasks = self._sort_tasks_by_priority()

        for task in sorted_tasks:
            if not self._assign_task(task):
                self.unassigned_reasons[task.id] = self._get_all_unassignment_reasons(task)

        return len(self.schedule.get_unassigned_tasks()) == 0

    def _sort_tasks_by_priority(self) -> List[Task]:
        """
        Sort tasks by priority (high to low) and then by deadline.

        Returns:
            Sorted list of tasks
        """
        return sorted(
            self.schedule.tasks,
            key=lambda t: (
                -t.priority,  # Higher priority first (negative for descending)
                t.deadline if t.deadline else float('inf')  # Earlier deadline first
            )
        )

    def _assign_task(self, task: Task) -> bool:
        """
        Assign a task to the best available employee.

        Args:
            task: The task to assign

        Returns:
            True if task was assigned, False otherwise
        """
        eligible_employees = self._get_eligible_employees(task)

        if not eligible_employees:
            return False

        best_employee = self._select_best_employee(task, eligible_employees)
        return task.assign_to(best_employee)

    def _get_eligible_employees(self, task: Task) -> List[Employee]:
        """
        Get all employees who can perform the task.

        Args:
            task: The task to check

        Returns:
            List of eligible employees
        """
        return [
            emp for emp in self.schedule.employees
            if task.can_be_assigned_to(emp)
        ]

    def _select_best_employee(self, task: Task, eligible_employees: List[Employee]) -> Employee:
        """
        Select the best employee for a task based on a scoring system.

        Scoring criteria:
        - Rank appropriateness (prefer employees close to min_rank)
        - Available hours (prefer employees with more availability)
        - Current workload (prefer less loaded employees)

        Args:
            task: The task to assign
            eligible_employees: List of eligible employees

        Returns:
            The best employee for the task
        """
        scored_employees = [
            (emp, self._score_employee_for_task(task, emp))
            for emp in eligible_employees
        ]

        scored_employees.sort(key=lambda x: x[1], reverse=True)
        return scored_employees[0][0]

    def _score_employee_for_task(self, task: Task, employee: Employee) -> float:
        """
        Calculate a score for how well an employee fits a task.

        Args:
            task: The task to score for
            employee: The employee to score

        Returns:
            Score (higher is better)
        """
        score = 0.0

        # Rank appropriateness (prefer employees close to min_rank to avoid over-qualification)
        rank_diff = employee.rank - task.min_rank
        if rank_diff == 0:
            score += 50  # Perfect match
        elif rank_diff <= 2:
            score += 40  # Close match
        elif rank_diff <= 4:
            score += 20  # Acceptable match
        else:
            score += 10  # Over-qualified (less preferred)

        # Available hours (prefer employees with more availability)
        availability_ratio = employee.available_hours() / employee.max_hours
        score += availability_ratio * 30

        # Current workload (prefer less loaded employees for balance)
        workload_ratio = 1 - (employee.current_hours / employee.max_hours)
        score += workload_ratio * 20

        return score

    def _get_all_unassignment_reasons(self, task: Task) -> List[str]:
        """
        Get reasons why a task couldn't be assigned to any employee.

        Args:
            task: The unassigned task

        Returns:
            List of reasons across all employees
        """
        if not self.schedule.employees:
            return ["No employees available"]

        all_reasons = set()
        for employee in self.schedule.employees:
            reasons = task.get_unassignment_reasons(employee)
            all_reasons.update(reasons)

        if not all_reasons:
            return ["Unknown reason (this shouldn't happen)"]

        return list(all_reasons)

    def get_unassigned_tasks_report(self) -> List[Dict]:
        """
        Get a detailed report of unassigned tasks with reasons.

        Returns:
            List of dictionaries with task info and reasons
        """
        report = []
        for task in self.schedule.get_unassigned_tasks():
            report.append({
                'task_id': task.id,
                'task_name': task.name,
                'priority': task.priority,
                'duration': task.duration,
                'required_training': list(task.required_training),
                'min_rank': task.min_rank,
                'reasons': self.unassigned_reasons.get(task.id, ["Unknown"])
            })
        return report

    def get_employee_workload_report(self) -> List[Dict]:
        """
        Get a report of employee workloads.

        Returns:
            List of dictionaries with employee workload info
        """
        report = []
        for employee in self.schedule.employees:
            tasks = self.schedule.get_employee_tasks(employee)
            report.append({
                'employee_id': employee.id,
                'employee_name': employee.name,
                'position': employee.position,
                'rank': employee.rank,
                'assigned_hours': employee.current_hours,
                'max_hours': employee.max_hours,
                'available_hours': employee.available_hours(),
                'utilization': round((employee.current_hours / employee.max_hours) * 100, 2) if employee.max_hours > 0 else 0,
                'task_count': len(tasks),
                'tasks': [{'id': t.id, 'name': t.name, 'duration': t.duration} for t in tasks]
            })
        return sorted(report, key=lambda x: x['utilization'], reverse=True)
