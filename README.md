# PMO Project Plan & Status Dashboard: Oracle 21c Database Migration

A simulated PMO project built to practise project planning, scheduling, and status reporting. It is based on my hands-on experience with Oracle 21c database operations at Infosys.

> **Note:** This is a simulated project. The scope, budget, timeline, progress, and spend figures are illustrative assumptions, not real company data.

![PMO Dashboard](PMO_Dashboard.png)

## Project Overview

| Item | Detail |
|---|---|
| Project | Oracle 21c Database Migration & Upgrade Program |
| Objective | Migrate production Oracle databases to a new 21c environment with zero data loss and under 4 hours of planned downtime |
| Duration | 12 weeks (60 working days) |
| Budget | INR 25,00,000 |
| Tasks | 16 tasks across 6 phases (Planning, Setup, Migration, Testing, Go-Live, Handover) |
| Milestones | Plan approved, Environment ready, UAT sign-off, Go-live, Project closed |

## What's in this repository

| File | Description |
|---|---|
| `Oracle_Migration_Project_Plan.xlsx` | Excel workbook with the project charter, WBS and schedule, Gantt chart, and milestone tracker |
| `PMO_Dashboard.png` | Status dashboard image (simulated Week 9 status) |
| `pmo_dashboard.py` | Python script that generates the dashboard |
| `requirements.txt` | Python libraries needed to run the script |

## Excel workbook

- **Charter:** objective, scope, deliverables, stakeholders, success criteria, risks, budget, and overall % complete.
- **WBS_Schedule:** tasks with owner, duration, and dependencies. Start and end dates calculate automatically from the dependency chain.
- **Gantt:** weekly colour-coded chart by phase, with milestone markers. It updates when the schedule changes.
- **Milestones:** target dates and status for each milestone.

## Dashboard metrics

| Metric | Value (simulated) | How it is calculated |
|---|---|---|
| Overall progress | 70% | Completed working days / total working days |
| Budget used | INR 17.95 lakh (72%) | Actual spend to date / budget |
| Schedule Performance Index (SPI) | 0.98 | Earned Value / Planned Value |
| Cost Performance Index (CPI) | 0.97 | Earned Value / Actual Cost |
| Forecast at completion | INR 25.6 lakh (+2.6%) | Budget / CPI |

Key findings from the simulated Week 9 status:
- The project is 70% complete and overall status is Green.
- The forecast stays within the 5% budget tolerance set in the charter.
- UAT is the current critical task. All tasks are on the critical path, so any delay moves the Go-live date.

## How to run the dashboard script

```bash
pip install -r requirements.txt
python pmo_dashboard.py
```

This creates `PMO_Dashboard.png` in the same folder.

## Tools and skills

Excel, Python (matplotlib, numpy), Gantt charts, work breakdown structure, critical path, milestone tracking, earned value analysis (SPI, CPI), status reporting.

## Author

**Reshma Vinnapala**
B.Tech in Electrical and Electronics Engineering | Ex-Infosys System Engineer Trainee (Oracle 21c DBA)
LinkedIn: *www.linkedin.com/in/reshma-vinnapala*
