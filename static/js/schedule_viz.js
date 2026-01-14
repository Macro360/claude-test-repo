// Schedule visualization using Chart.js

function createWorkloadChart(workloadData) {
    const ctx = document.getElementById('workloadChart');
    if (!ctx) return;

    const labels = workloadData.map(emp => emp.employee_name);
    const assignedHours = workloadData.map(emp => emp.assigned_hours);
    const maxHours = workloadData.map(emp => emp.max_hours);
    const availableHours = workloadData.map(emp => emp.available_hours);

    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Assigned Hours',
                    data: assignedHours,
                    backgroundColor: 'rgba(52, 152, 219, 0.8)',
                    borderColor: 'rgba(52, 152, 219, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Available Hours',
                    data: availableHours,
                    backgroundColor: 'rgba(46, 204, 113, 0.8)',
                    borderColor: 'rgba(46, 204, 113, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Employee Workload Distribution',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        afterLabel: function(context) {
                            const index = context.dataIndex;
                            const emp = workloadData[index];
                            return [
                                `Max Hours: ${emp.max_hours}h`,
                                `Utilization: ${emp.utilization}%`,
                                `Tasks: ${emp.task_count}`
                            ];
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Hours'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Employees'
                    }
                }
            }
        }
    });

    return chart;
}

function createUtilizationChart(workloadData) {
    const ctx = document.getElementById('utilizationChart');
    if (!ctx) return;

    const labels = workloadData.map(emp => emp.employee_name);
    const utilization = workloadData.map(emp => emp.utilization);

    const backgroundColors = utilization.map(util => {
        if (util > 90) return 'rgba(231, 76, 60, 0.8)';  // Red - overutilized
        if (util > 70) return 'rgba(243, 156, 18, 0.8)';  // Orange - high
        return 'rgba(46, 204, 113, 0.8)';  // Green - good
    });

    const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: 'Utilization %',
                data: utilization,
                backgroundColor: backgroundColors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Employee Utilization Percentage',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: true,
                    position: 'right'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const emp = workloadData[context.dataIndex];
                            return [
                                `${context.label}: ${context.parsed}%`,
                                `Hours: ${emp.assigned_hours}/${emp.max_hours}h`,
                                `Tasks: ${emp.task_count}`
                            ];
                        }
                    }
                }
            }
        }
    });

    return chart;
}

function createTaskDistributionChart(workloadData) {
    const ctx = document.getElementById('taskDistributionChart');
    if (!ctx) return;

    const labels = workloadData.map(emp => emp.employee_name);
    const taskCounts = workloadData.map(emp => emp.task_count);

    const chart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Tasks Assigned',
                data: taskCounts,
                backgroundColor: [
                    'rgba(52, 152, 219, 0.8)',
                    'rgba(46, 204, 113, 0.8)',
                    'rgba(155, 89, 182, 0.8)',
                    'rgba(241, 196, 15, 0.8)',
                    'rgba(230, 126, 34, 0.8)',
                    'rgba(231, 76, 60, 0.8)',
                    'rgba(149, 165, 166, 0.8)',
                    'rgba(52, 73, 94, 0.8)'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Task Distribution Among Employees',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: true,
                    position: 'bottom'
                }
            }
        }
    });

    return chart;
}

// Initialize charts when data is available
document.addEventListener('DOMContentLoaded', function() {
    // Charts will be initialized from the template with specific data
    if (typeof workloadData !== 'undefined' && workloadData.length > 0) {
        createWorkloadChart(workloadData);
    }
});
