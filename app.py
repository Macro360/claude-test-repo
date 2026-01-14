"""
Flask web application for the automatic scheduling system.
"""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from datetime import datetime
from models import Employee, Task, Schedule
from scheduler import AutoScheduler
from export_handlers import JSONExporter, CSVExporter, ReportGenerator
from utils import get_current_two_week_period, parse_training_list, format_training_list, get_period_description
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Session data keys
EMPLOYEES_KEY = 'employees'
TASKS_KEY = 'tasks'
SCHEDULE_KEY = 'schedule'
NEXT_EMP_ID = 'next_emp_id'
NEXT_TASK_ID = 'next_task_id'


def init_session():
    """Initialize session data if not present."""
    if EMPLOYEES_KEY not in session:
        session[EMPLOYEES_KEY] = []
    if TASKS_KEY not in session:
        session[TASKS_KEY] = []
    if NEXT_EMP_ID not in session:
        session[NEXT_EMP_ID] = 1
    if NEXT_TASK_ID not in session:
        session[NEXT_TASK_ID] = 1


def get_employees():
    """Get employees from session as Employee objects."""
    init_session()
    employees = []
    for emp_data in session[EMPLOYEES_KEY]:
        employees.append(Employee(
            id=emp_data['id'],
            name=emp_data['name'],
            training=set(emp_data['training']),
            rank=emp_data['rank'],
            position=emp_data['position'],
            max_hours=emp_data['max_hours'],
            current_hours=emp_data.get('current_hours', 0.0)
        ))
    return employees


def get_tasks():
    """Get tasks from session as Task objects."""
    init_session()
    tasks = []
    employees = get_employees()
    emp_dict = {emp.id: emp for emp in employees}

    for task_data in session[TASKS_KEY]:
        task = Task(
            id=task_data['id'],
            name=task_data['name'],
            required_training=set(task_data['required_training']),
            duration=task_data['duration'],
            priority=task_data['priority'],
            min_rank=task_data['min_rank']
        )
        if task_data.get('assigned_employee_id'):
            task.assigned_employee = emp_dict.get(task_data['assigned_employee_id'])
            if task.assigned_employee:
                task.assigned_employee.current_hours = task_data.get('assigned_hours', 0.0)
        tasks.append(task)
    return tasks


def save_employees(employees):
    """Save employees to session."""
    session[EMPLOYEES_KEY] = [emp.to_dict() for emp in employees]
    session.modified = True


def save_tasks(tasks):
    """Save tasks to session."""
    task_data = []
    for task in tasks:
        data = task.to_dict()
        if task.assigned_employee:
            data['assigned_hours'] = task.assigned_employee.current_hours
        task_data.append(data)
    session[TASKS_KEY] = task_data
    session.modified = True


def get_current_schedule():
    """Get current schedule object."""
    employees = get_employees()
    tasks = get_tasks()
    period_start, period_end = get_current_two_week_period()
    return Schedule(
        employees=employees,
        tasks=tasks,
        period_start=period_start,
        period_end=period_end
    )


@app.route('/')
def index():
    """Home page / dashboard."""
    init_session()
    schedule = get_current_schedule()
    stats = schedule.get_statistics()
    period_start, period_end = get_current_two_week_period()

    return render_template('index.html',
                         stats=stats,
                         period_description=get_period_description(period_start, period_end),
                         employee_count=len(schedule.employees),
                         task_count=len(schedule.tasks))


@app.route('/employees')
def manage_employees():
    """View and manage employees."""
    employees = get_employees()
    return render_template('manage_employees.html', employees=employees)


@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    """Add a new employee."""
    if request.method == 'POST':
        init_session()
        name = request.form.get('name')
        position = request.form.get('position')
        rank = int(request.form.get('rank', 1))
        max_hours = float(request.form.get('max_hours', 80))
        training_str = request.form.get('training', '')
        training = parse_training_list(training_str)

        emp_id = session[NEXT_EMP_ID]
        session[NEXT_EMP_ID] = emp_id + 1

        employee = Employee(
            id=emp_id,
            name=name,
            training=training,
            rank=rank,
            position=position,
            max_hours=max_hours
        )

        employees = get_employees()
        employees.append(employee)
        save_employees(employees)

        return redirect(url_for('manage_employees'))

    return render_template('add_employee.html')


@app.route('/employees/delete/<int:emp_id>', methods=['POST'])
def delete_employee(emp_id):
    """Delete an employee."""
    employees = get_employees()
    employees = [emp for emp in employees if emp.id != emp_id]
    save_employees(employees)

    # Also unassign any tasks assigned to this employee
    tasks = get_tasks()
    for task in tasks:
        if task.assigned_employee and task.assigned_employee.id == emp_id:
            task.unassign()
    save_tasks(tasks)

    return redirect(url_for('manage_employees'))


@app.route('/tasks')
def manage_tasks():
    """View and manage tasks."""
    tasks = get_tasks()
    return render_template('manage_tasks.html', tasks=tasks)


@app.route('/tasks/add', methods=['GET', 'POST'])
def add_task():
    """Add a new task."""
    if request.method == 'POST':
        init_session()
        name = request.form.get('name')
        duration = float(request.form.get('duration', 1))
        priority = int(request.form.get('priority', 5))
        min_rank = int(request.form.get('min_rank', 1))
        training_str = request.form.get('required_training', '')
        required_training = parse_training_list(training_str)

        task_id = session[NEXT_TASK_ID]
        session[NEXT_TASK_ID] = task_id + 1

        task = Task(
            id=task_id,
            name=name,
            required_training=required_training,
            duration=duration,
            priority=priority,
            min_rank=min_rank
        )

        tasks = get_tasks()
        tasks.append(task)
        save_tasks(tasks)

        return redirect(url_for('manage_tasks'))

    return render_template('add_task.html')


@app.route('/tasks/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """Delete a task."""
    tasks = get_tasks()
    tasks = [task for task in tasks if task.id != task_id]
    save_tasks(tasks)
    return redirect(url_for('manage_tasks'))


@app.route('/schedule/generate', methods=['POST'])
def generate_schedule():
    """Generate the schedule using the scheduler algorithm."""
    schedule = get_current_schedule()
    scheduler = AutoScheduler(schedule)
    scheduler.schedule_all()

    # Save the updated schedule back to session
    save_employees(schedule.employees)
    save_tasks(schedule.tasks)

    return redirect(url_for('view_schedule'))


@app.route('/schedule/view')
def view_schedule():
    """View the generated schedule."""
    schedule = get_current_schedule()
    scheduler = AutoScheduler(schedule)

    employee_workload = scheduler.get_employee_workload_report()
    unassigned_tasks = scheduler.get_unassigned_tasks_report() if schedule.get_unassigned_tasks() else []

    period_start, period_end = get_current_two_week_period()

    return render_template('schedule.html',
                         schedule=schedule,
                         employee_workload=employee_workload,
                         unassigned_tasks=unassigned_tasks,
                         period_description=get_period_description(period_start, period_end))


@app.route('/schedule/reset', methods=['POST'])
def reset_schedule():
    """Reset all task assignments."""
    schedule = get_current_schedule()
    schedule.reset()
    save_employees(schedule.employees)
    save_tasks(schedule.tasks)
    return redirect(url_for('index'))


@app.route('/export')
def export_page():
    """Export options page."""
    schedule = get_current_schedule()
    return render_template('export.html', schedule=schedule)


@app.route('/export/json')
def export_json():
    """Export schedule as JSON."""
    schedule = get_current_schedule()
    json_data = JSONExporter.export(schedule)

    response = make_response(json_data)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = 'attachment; filename=schedule.json'
    return response


@app.route('/export/csv/<export_type>')
def export_csv(export_type):
    """Export schedule as CSV."""
    schedule = get_current_schedule()

    if export_type == 'employees':
        csv_data = CSVExporter.export_employees(schedule)
        filename = 'employees.csv'
    elif export_type == 'tasks':
        csv_data = CSVExporter.export_tasks(schedule)
        filename = 'tasks.csv'
    else:
        csv_data = CSVExporter.export_schedule(schedule)
        filename = 'schedule.csv'

    response = make_response(csv_data)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return response


@app.route('/export/report/<report_type>')
def export_report(report_type):
    """Export schedule as text report."""
    schedule = get_current_schedule()
    scheduler = AutoScheduler(schedule)

    if report_type == 'summary':
        report = ReportGenerator.generate_summary(schedule, scheduler)
        filename = 'summary.txt'
    elif report_type == 'employees':
        report = ReportGenerator.generate_employee_report(schedule, scheduler)
        filename = 'employee_report.txt'
    elif report_type == 'tasks':
        report = ReportGenerator.generate_task_report(schedule, scheduler)
        filename = 'task_report.txt'
    else:
        report = ReportGenerator.generate_full_report(schedule, scheduler)
        filename = 'full_report.txt'

    response = make_response(report)
    response.headers['Content-Type'] = 'text/plain'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return response


@app.route('/data/clear', methods=['POST'])
def clear_data():
    """Clear all data from session."""
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
