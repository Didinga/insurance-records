# Insurance Records

![Python](https://img.shields.io/badge/Python-3.8-blue)
![Django](https://img.shields.io/badge/Django-4.x-green)

A Django web application for managing insured persons and their insurance records. Supports user authentication with role-based access — only admins can add, edit, or delete records.

## Features

- List of all insured persons sorted by last name
- Detail view for each insured person
- Add, edit and delete insured persons (admin only)
- User registration and login via email
- Role-based permissions (admin vs regular user)
- Multiple insurance types and details per person

## Tech Stack

- Python 3.8
- Django
- SQLite (development)

## Installation

```bash
git clone https://github.com/Didinga/insurance-records.git
cd insurance-records
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Usage

Open your browser at `http://127.0.0.1:8000`

- Register a new account or log in
- Browse the list of insured persons
- Admins can add, edit and delete records

## Models

- `Insurance` - insurance type (e.g. life, health, car)
- `InsuranceDetail` - additional detail for an insurance
- `InsuredPerson` - person with first name, last name, age, address, insurance type and details
- `User` - custom user model using email instead of username

## Author

Didinga Omodi - [GitHub](https://github.com/Didinga) - [LinkedIn](https://www.linkedin.com/in/didiomodi/)
