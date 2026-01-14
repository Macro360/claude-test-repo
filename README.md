# Automatic Scheduling System

A comprehensive web-based employee scheduling system that automatically assigns tasks to employees based on their training, rank, position, and hour availability. Built with Python Flask and designed for 2-week scheduling periods.

## Features

### Core Functionality
- **Intelligent Task Assignment**: Automatically assigns tasks to employees using a constraint-based scheduling algorithm
- **Employee Management**: Track employees with their skills, rank (1-10), position, and hour limits
- **Task Management**: Define tasks with required skills, duration, priority (1-10), and minimum rank requirements
- **2-Week Scheduling Periods**: Optimized for bi-weekly work schedules
- **Constraint Satisfaction**: Ensures all assignments respect employee qualifications and hour limits

### Smart Scheduling Algorithm
- **Priority-Based**: High-priority tasks are assigned first
- **Rank-Aware**: Matches employee ranks to task requirements, avoiding over/under-qualification
- **Training Matching**: Verifies employees have all required skills
- **Hour Balancing**: Distributes workload while respecting hour limits
- **Detailed Reporting**: Provides reasons when tasks cannot be assigned

### Multiple Export Formats
- **JSON**: Complete schedule data for programmatic use
- **CSV**: Separate exports for employees, tasks, and complete schedule
- **Text Reports**: Human-readable reports including:
  - Summary report with statistics
  - Employee workload report
  - Task assignment report
  - Full comprehensive report

### Visual Interface
- **Interactive Dashboard**: Real-time schedule statistics
- **Workload Charts**: Visual representation using Chart.js
- **Employee Utilization**: Track hour usage and availability
- **Task Status**: See assigned and unassigned tasks at a glance

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd claude-test-repo
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the web interface**
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage Guide

### 1. Add Employees

Navigate to **Employees** → **Add Employee**

Fill in the following information:
- **Name**: Employee's full name
- **Position**: Job title (e.g., "Software Engineer", "Designer")
- **Rank**: Seniority level from 1-10 (1 = Junior, 10 = Senior)
- **Max Hours**: Maximum hours for the 2-week period (e.g., 80 hours)
- **Training/Skills**: Comma-separated list of skills (e.g., "Python, JavaScript, Leadership")

### 2. Add Tasks

Navigate to **Tasks** → **Add Task**

Fill in the following information:
- **Task Name**: Descriptive name of the task
- **Duration**: Hours required to complete the task
- **Priority**: Task priority from 1-10 (1 = Low, 10 = High)
- **Minimum Rank**: Minimum employee rank required (1-10)
- **Required Skills**: Comma-separated list of required skills

### 3. Generate Schedule

1. Go to the **Dashboard**
2. Click **Generate Schedule**
3. The system will automatically assign tasks to employees based on:
   - Employee training matching task requirements
   - Employee rank meeting minimum requirements
   - Available hours within the 2-week period
   - Task priority (higher priority tasks assigned first)

### 4. View Schedule

Navigate to **Schedule** to see:
- Employee workload distribution (chart and details)
- Individual employee assignments
- Task completion status
- Unassigned tasks with detailed reasons

### 5. Export Schedule

Navigate to **Export** to download the schedule in various formats:

**JSON Export**:
- Complete schedule data
- Includes all employees, tasks, and assignments

**CSV Exports**:
- Complete Schedule: All assignments
- Employees Only: Employee data with hours
- Tasks Only: Task data with assignments

**Text Reports**:
- Full Report: Complete detailed report
- Summary: Overview statistics
- Employee Report: Workload details per employee
- Task Report: Assignment details per task

### 6. Manage Data

**Edit Employees/Tasks**: View lists in the management pages and delete as needed

**Reset Schedule**: Clear all assignments while keeping employee and task data

**Clear All Data**: Remove all employees, tasks, and assignments (start fresh)

## System Architecture

### Backend Components

**models.py** - Data Models
- `Employee`: Represents an employee with skills, rank, position, and hour limits
- `Task`: Represents a task with requirements, duration, and priority
- `Schedule`: Container for employees and tasks with statistics

**scheduler.py** - Scheduling Engine
- `AutoScheduler`: Implements the constraint-based scheduling algorithm
- Scoring system for optimal employee-task matching
- Detailed reporting for unassigned tasks

**utils.py** - Utility Functions
- Date handling for 2-week periods
- Validation functions
- Data parsing and formatting

**export_handlers.py** - Export Functionality
- `JSONExporter`: JSON format exports
- `CSVExporter`: CSV format exports
- `ReportGenerator`: Text report generation

**app.py** - Flask Web Application
- Route definitions for all pages
- Session management for data storage
- Integration with scheduler and exporters

### Frontend Components

**templates/** - HTML Templates
- `base.html`: Base layout with navigation
- `index.html`: Dashboard with statistics
- `add_employee.html` / `manage_employees.html`: Employee management
- `add_task.html` / `manage_tasks.html`: Task management
- `schedule.html`: Schedule visualization
- `export.html`: Export options

**static/css/style.css** - Styling
- Professional, responsive design
- Color-coded status indicators
- Mobile-friendly layout

**static/js/** - JavaScript
- `script.js`: Form validation and interactivity
- `schedule_viz.js`: Chart.js visualizations

## Scheduling Algorithm Details

The scheduler uses a greedy algorithm with constraint satisfaction:

1. **Sort Tasks**: By priority (descending) and deadline
2. **For Each Task**:
   - Find eligible employees (have required training, sufficient rank, available hours)
   - Score each eligible employee:
     - Rank appropriateness (prefer close match to minimum rank)
     - Available hours (prefer more availability)
     - Current workload (prefer balanced distribution)
   - Assign to highest-scoring employee
3. **Track Failures**: Record detailed reasons for unassigned tasks

### Constraints

**Hard Constraints** (Must satisfy):
- Employee must have ALL required training/skills
- Employee must have sufficient hours available
- Employee rank must meet minimum requirement

**Soft Constraints** (Optimized):
- Higher priority tasks assigned first
- Balanced workload distribution
- Appropriate rank matching (avoid over-qualification)

## Configuration

### Session Secret Key

For production use, change the secret key in `app.py`:
```python
app.secret_key = 'your-secure-secret-key-here'
```

Generate a secure key with:
```python
import secrets
print(secrets.token_hex(32))
```

### Port Configuration

Default port is 5000. To change, modify `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=YOUR_PORT)
```

## Data Storage

The application uses Flask sessions for data storage, which means:
- Data is stored in browser cookies (encrypted)
- Data persists across page refreshes
- Data is cleared when you use "Clear All Data" or clear browser cookies
- For persistent storage, the system can be extended to use SQLite or PostgreSQL

## Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Kill process using port 5000 (Linux/Mac)
lsof -ti:5000 | xargs kill -9

# Or use a different port
python app.py --port 5001
```

**Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Session Data Lost**
- Check browser cookie settings
- Ensure cookies are enabled
- Try clearing browser cache and restarting

### Debug Mode

The application runs in debug mode by default. For production:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## Technical Specifications

- **Framework**: Flask 3.0.0
- **Python Version**: 3.8+
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Visualization**: Chart.js 4.4.0
- **Data Format**: JSON, CSV, Plain Text
- **Session Management**: Flask Sessions
- **Architecture**: MVC Pattern

## Future Enhancements

Potential improvements for future versions:
- Database integration (SQLite/PostgreSQL)
- User authentication and multi-user support
- Calendar view with drag-and-drop
- Email notifications
- Advanced scheduling algorithms (genetic algorithms, constraint programming)
- REST API for external integrations
- Mobile app support
- Recurring task templates
- Shift scheduling support
- Time-off management

## Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for educational and commercial use.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Review the documentation above
- Check the troubleshooting section

## Acknowledgments

Built with:
- Flask web framework
- Chart.js for visualizations
- Modern HTML5/CSS3 standards

---

**Version**: 1.0.0
**Last Updated**: January 2026
