## 🏢 Job Portal
A full‑featured job portal built using Django and Bootstrap, designed for
- Employers to post jobs, manage listings, and review applicants.
- Job seekers to create profiles, search and save jobs, and submit applications.

## 🚀 Features
✅ Custom user roles: Employers vs. job seekers
📝 User registration/login with role‑based dashboard
🏢 Employer Dashboard – post/edit/delete jobs, view applications
🔍 Job listings with search & filters (keyword, category, location, type)
💾 Save/bookmark jobs for later
📄 Resume upload and seeker profile management
📨 Email notifications on application submission & status changes
📊 Application status tracking (pending, reviewed, shortlisted, rejected)
📱 Responsive UI powered by Bootstrap
🧪 Automated tests and GitHub Actions CI workflow

## 🧩 Tech Stack
- 🐍 Python 3.11
- ⚙️ Django 5.2
- 🗄️ SQLite (development)
- 🎨 Bootstrap 5
- 💾 Media storage for resumes/logos/profile pics
- ✅ GitHub Actions for CI (migrations + tests)
- 🛠️ Environment: virtualenv / venv

## 📁 Repository Structure
```
jobportal_project/
├── apps/
│   ├── accounts/          # user authentication & profiles
│   ├── jobs/              # job posting & management
│   └── applications/      # job applications & tracking
├── config/                # Django settings & URLs
├── media/                 # user-uploaded files (resumes, logos)
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── .github/
│   └── workflows/         # GitHub Actions CI
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── README.md              # project documentation
├── LICENSE                # MIT license
└── .gitignore             # files to ignore in Git
```


## ⚙️ Setup Instructions
```bash
# clone repo
git clone https://github.com/<your‑user>/jobportal_project.git
cd jobportal_project
# create & activate environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
# install dependencies
pip install -r requirements.txt
# run migrations
python manage.py migrate
# create superuser (optional)
python manage.py createsuperuser
# start development server
python manage.py runserver
```
## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.


