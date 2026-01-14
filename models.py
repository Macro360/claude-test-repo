"""
Data models for the automatic scheduling system.
"""
from dataclasses import dataclass, field
from typing import List, Set, Optional
from datetime import datetime


@dataclass
class Employee:
    """Represents an employee with their qualifications and constraints."""

    id: int
    name: str
    training: Set[str]  # Skills/certifications the employee has
    rank: int  # Employee rank (1-10, higher = more senior)
    position: str  # Job title/position
    max_hours: float  # Maximum hours per 2-week period
    current_hours: float = 0.0  # Currently assigned hours

    def has_training(self, required_training: Set[str]) -> bool:
        """Check if employee has all required training."""
        return required_training.issubset(self.training)

    def can_work_hours(self, hours: float) -> bool:
        """Check if employee can work additional hours."""
        return (self.current_hours + hours) <= self.max_hours

    def assign_hours(self, hours: float) -> None:
        """Assign hours to this employee."""
        self.current_hours += hours

    def reset_hours(self) -> None:
        """Reset current hours to 0."""
        self.current_hours = 0.0

    def available_hours(self) -> float:
        """Get remaining available hours."""
        return max(0, self.max_hours - self.current_hours)

    def to_dict(self) -> dict:
        """Convert employee to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'training': list(self.training),
            'rank': self.rank,
            'position': self.position,
            'max_hours': self.max_hours,
            'current_hours': self.current_hours,
            'available_hours': self.available_hours()
        }

    def __repr__(self) -> str:
        return (f"Employee(id={self.id}, name='{self.name}', "
                f"rank={self.rank}, position='{self.position}', "
                f"hours={self.current_hours}/{self.max_hours})")


@dataclass
class Task:
    """Represents a task that needs to be scheduled."""

    id: int
    name: str
    required_training: Set[str]  # Required skills for this task
    duration: float  # Duration in hours
    priority: int  # Task priority (1-10, higher = more important)
    min_rank: int = 1  # Minimum rank required
    deadline: Optional[datetime] = None
    assigned_employee: Optional[Employee] = None

    def is_assigned(self) -> bool:
        """Check if task is assigned to an employee."""
        return self.assigned_employee is not None

    def can_be_assigned_to(self, employee: Employee) -> bool:
        """Check if task can be assigned to given employee."""
        return (
            employee.has_training(self.required_training) and
            employee.can_work_hours(self.duration) and
            employee.rank >= self.min_rank
        )

    def assign_to(self, employee: Employee) -> bool:
        """Assign task to employee. Returns True if successful."""
        if self.can_be_assigned_to(employee):
            self.assigned_employee = employee
            employee.assign_hours(self.duration)
            return True
        return False

    def unassign(self) -> None:
        """Unassign task from current employee."""
        if self.assigned_employee:
            self.assigned_employee.current_hours -= self.duration
            self.assigned_employee = None

    def get_unassignment_reasons(self, employee: Employee) -> List[str]:
        """Get reasons why task cannot be assigned to employee."""
        reasons = []
        if not employee.has_training(self.required_training):
            missing = self.required_training - employee.training
            reasons.append(f"Missing required training: {', '.join(missing)}")
        if not employee.can_work_hours(self.duration):
            reasons.append(f"Insufficient hours available ({employee.available_hours()}h available, {self.duration}h needed)")
        if employee.rank < self.min_rank:
            reasons.append(f"Rank too low (rank {employee.rank}, minimum {self.min_rank} required)")
        return reasons

    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'required_training': list(self.required_training),
            'duration': self.duration,
            'priority': self.priority,
            'min_rank': self.min_rank,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'assigned_employee_id': self.assigned_employee.id if self.assigned_employee else None,
            'assigned_employee_name': self.assigned_employee.name if self.assigned_employee else None,
            'is_assigned': self.is_assigned()
        }

    def __repr__(self) -> str:
        assigned_to = self.assigned_employee.name if self.assigned_employee else "Unassigned"
        return (f"Task(id={self.id}, name='{self.name}', "
                f"duration={self.duration}h, priority={self.priority}, "
                f"assigned_to='{assigned_to}')")


@dataclass
class Schedule:
    """Represents a complete schedule with task assignments."""

    employees: List[Employee]
    tasks: List[Task]
    period_start: datetime
    period_end: datetime
    created_at: datetime = field(default_factory=datetime.now)

    def get_assigned_tasks(self) -> List[Task]:
        """Get all assigned tasks."""
        return [task for task in self.tasks if task.is_assigned()]

    def get_unassigned_tasks(self) -> List[Task]:
        """Get all unassigned tasks."""
        return [task for task in self.tasks if not task.is_assigned()]

    def get_employee_tasks(self, employee: Employee) -> List[Task]:
        """Get all tasks assigned to a specific employee."""
        return [task for task in self.tasks if task.assigned_employee == employee]

    def get_completion_rate(self) -> float:
        """Get percentage of tasks that are assigned."""
        if not self.tasks:
            return 100.0
        return (len(self.get_assigned_tasks()) / len(self.tasks)) * 100

    def is_valid(self) -> bool:
        """Check if schedule is valid (no constraint violations)."""
        for employee in self.employees:
            if employee.current_hours > employee.max_hours:
                return False

        for task in self.get_assigned_tasks():
            if task.assigned_employee and not task.can_be_assigned_to(task.assigned_employee):
                return False

        return True

    def reset(self) -> None:
        """Reset all assignments."""
        for employee in self.employees:
            employee.reset_hours()
        for task in self.tasks:
            task.unassign()

    def get_statistics(self) -> dict:
        """Get schedule statistics."""
        return {
            'total_employees': len(self.employees),
            'total_tasks': len(self.tasks),
            'assigned_tasks': len(self.get_assigned_tasks()),
            'unassigned_tasks': len(self.get_unassigned_tasks()),
            'completion_rate': round(self.get_completion_rate(), 2),
            'total_hours_scheduled': sum(emp.current_hours for emp in self.employees),
            'average_hours_per_employee': round(sum(emp.current_hours for emp in self.employees) / len(self.employees), 2) if self.employees else 0,
            'is_valid': self.is_valid()
        }

    def to_dict(self) -> dict:
        """Convert schedule to dictionary for JSON serialization."""
        return {
            'period_start': self.period_start.isoformat(),
            'period_end': self.period_end.isoformat(),
            'created_at': self.created_at.isoformat(),
            'statistics': self.get_statistics(),
            'employees': [emp.to_dict() for emp in self.employees],
            'tasks': [task.to_dict() for task in self.tasks]
        }
