# Manpower Database Management and Automation System (MDMAS)

MDMAS is a Flask-based web application designed to manage the database and processes for employees traveling abroad for work. The system links employees with employers, tracks brokers, and automates various administrative workflows.

## Features

- Record and manage data about:
  - Employees traveling abroad
  - Their employers
  - Brokers who facilitated their employment
- Schedule and send automated emails and SMS for:
  - OPD test reminders
  - Police checks
  - Air ticket coordination
- Notify staff of urgent or pending tasks
- Automatically generate a CV for each employee using stored data
- User authentication via Flask Blueprints (see `auth/` folder)

## Tech Stack

- Python
- Flask
- SQLite or MySQL (based on your configuration)
- Email & SMS integration (planned or in progress)

## Project Structure

- `application.py`: Main Flask application entry point
- `auth/`: Contains the authentication blueprint
- `templates/`, `static/`: Standard Flask web files

> Note: This project is currently in development and not yet deployed.

## Getting Started

To run the app locally:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python application.py
