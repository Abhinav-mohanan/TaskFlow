# TaskFlow

TaskFlow is a modern task management web application built with Django 6 and MongoDB, designed to improve personal productivity through secure authentication and structured task planning.

Instead of a standard relational database, this project uses MongoDB as the backend via ``django-mongodb-backend`` to handle the data storage

## Features

### Authentication & Security

* **Secure Signup:** Email-based registration with automatic OTP (One-Time Password) verification.
* **Flexible Login:** Access accounts using a traditional password or password-less email OTP.
* **Smart Reactivation:** Inactive accounts automatically trigger a new verification OTP upon login attempts.

### Task Management
* **Comprehensive CRUD:** Create, read, update, delete, and toggle completion status for tasks.
* **Dynamic Dashboard:** Quick summaries of tasks for "Today", "Upcoming", and overall status breakdowns.
* **Advanced Organization:** Filter and search tasks by priority, status and category.
* **Calendar View:** Visual task planning based on due dates and times.



## Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python & Django |
| **Database** | MongoDB (via django-mongodb-backend) |
| **Environment Management** | django-environ |
| **Frontend** | HTML/Django Templates, Tailwind CSS (via CDN) |


##  Installation & Setup

### Prerequisites
- Python 3.12+
- MongoDB

### Clone and Install

```bash
# Clone the repository
git clone https://github.com/Abhinav-mohanan/TaskFlow.git

# Create virtual environment
python -m venv env
source env/bin/activate   # or env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```
### Configure environment variables
Create a .env file in the root directory and configure your variables:

``` bash
DEBUG=True # Set False in production
SECRET_KEY=your_django_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1,api.yourdomain.com

MONGO_URI=mongodb://localhost:27017/ or MONGOURI

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

```
### Database Initialization & Run
Ensure your MongoDB service is running, then apply migrations and start the server:

``` bash
python manage.py migrate
python manage.py runserver

```

## Project Structure
```text
TaskFlow/
├── TaskFlow/              # Core Django project (settings, urls, wsgi, asgi)
├── apps/                  # Modular Django apps
│   ├── authentication/    # Custom user model, signup/login, and OTP flows
│   └── tasks/             # Task models, forms, views, and specific templates
├── templates/             # Shared global base templates
├── mongo_migrations/      # MongoDB-compatible migration modules
├── manage.py              # Django CLI utility
├── requirements.txt       # Project dependencies
└── .env                   # Environment variables (not tracked by git)

```

## 👨‍💻 Author
Abhinav Mohanan  
*Software Engineer*  

📧 Email: abhinavmohanan018@gmail.com


