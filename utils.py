"""
Utility functions for the scheduling system.
"""
from datetime import datetime, timedelta
from typing import Tuple


def get_current_two_week_period() -> Tuple[datetime, datetime]:
    """
    Get the current 2-week period starting from today.

    Returns:
        Tuple of (period_start, period_end)
    """
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    period_end = today + timedelta(days=13)  # 14 days total (0-13)
    return today, period_end


def get_two_week_period(start_date: datetime) -> Tuple[datetime, datetime]:
    """
    Get a 2-week period starting from the given date.

    Args:
        start_date: The start date of the period

    Returns:
        Tuple of (period_start, period_end)
    """
    period_start = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    period_end = period_start + timedelta(days=13)
    return period_start, period_end


def format_date(date: datetime) -> str:
    """Format a datetime object to a readable string."""
    return date.strftime('%Y-%m-%d')


def format_datetime(date: datetime) -> str:
    """Format a datetime object to a readable string with time."""
    return date.strftime('%Y-%m-%d %H:%M:%S')


def parse_date(date_str: str) -> datetime:
    """Parse a date string to a datetime object."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return datetime.fromisoformat(date_str)


def validate_rank(rank: int) -> bool:
    """Validate that rank is between 1 and 10."""
    return 1 <= rank <= 10


def validate_priority(priority: int) -> bool:
    """Validate that priority is between 1 and 10."""
    return 1 <= priority <= 10


def validate_hours(hours: float) -> bool:
    """Validate that hours is a positive number."""
    return hours > 0


def validate_training(training: str) -> bool:
    """Validate that training string is not empty."""
    return bool(training and training.strip())


def parse_training_list(training_str: str) -> set:
    """
    Parse a comma-separated string of training items into a set.

    Args:
        training_str: Comma-separated training items

    Returns:
        Set of training items
    """
    if not training_str:
        return set()
    return {item.strip() for item in training_str.split(',') if item.strip()}


def format_training_list(training_set: set) -> str:
    """
    Format a set of training items into a comma-separated string.

    Args:
        training_set: Set of training items

    Returns:
        Comma-separated string
    """
    return ', '.join(sorted(training_set))


def get_period_description(start: datetime, end: datetime) -> str:
    """
    Get a human-readable description of a time period.

    Args:
        start: Period start date
        end: Period end date

    Returns:
        Description string
    """
    return f"{format_date(start)} to {format_date(end)}"
