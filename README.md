# Job Portal Project

This is a Django-based job portal application developed as part of MCA coursework. It allows:

- Employers to post jobs, manage listings, and review applicants.
- Job seekers to create profiles, search and save jobs, and submit applications.

## Features

- Custom user roles (employer / seeker)
- Profile management with file uploads (logos, resumes)
- Job search with filters (keyword, category, location, type)
- Job bookmarking for seekers
- Application tracking and status updates
- Email notifications for applications and status changes
- Responsive Bootstrap-based UI

## Technologies

- Python 3.x
- Django 5.2
- SQLite3 (development)
- Bootstrap 5

## Setup

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

