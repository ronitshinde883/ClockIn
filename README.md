# Attendance Tracking System

A full-stack attendance management system built with **Django REST Framework** and **React**. The application allows teachers to create attendance sessions and students to mark their attendance using a **time-limited QR code**.

The goal is to make classroom attendance faster and reduce common problems such as manual attendance, proxy attendance, and maintaining attendance records manually.

---

## Features

### Teacher

* Create attendance sessions for a class
* Generate a dynamic QR code for attendance
* QR code automatically expires after a short period
* Monitor students who have marked attendance
* View attendance records
* View attendance statistics
* Manage courses/classes

### Student

* Login securely
* View enrolled courses
* Scan the attendance QR code
* Mark attendance for an active session
* View personal attendance history
* View attendance percentage for each course

### Attendance Security

* Time-limited QR codes
* QR codes are periodically refreshed
* Attendance can only be marked during an active session
* Server-side validation of attendance requests
* Prevent duplicate attendance submissions
* Authentication and authorization for different user roles

---

## How Attendance Works

The attendance system uses a temporary QR code to reduce proxy attendance.

```text
Teacher
   │
   ▼
Create Attendance Session
   │
   ▼
Server generates temporary QR token
   │
   ▼
QR Code displayed on teacher's screen
   │
   ▼
Student scans QR Code
   │
   ▼
React sends token to Django API
   │
   ▼
Django validates:
   ├── Is the session active?
   ├── Is the QR token valid?
   ├── Has the student already marked attendance?
   └── Is the request allowed?
   │
   ▼
Attendance Recorded
```

The QR token is periodically refreshed, so taking a screenshot of an old QR code should not allow attendance to be marked after the token expires.

---

## Tech Stack

### Backend

* **Python**
* **Django**
* **Django REST Framework**
* PostgreSQL
* JWT Authentication

### Frontend

* **React**
* JavaScript / TypeScript
* React Router
* Axios
* CSS / Tailwind CSS

### Development Tools

* Git
* GitHub
* VS Code
* Postman

Django provides the backend framework and ORM, while the React frontend communicates with the backend through REST APIs.

---

## Project Structure

```text
attendance-tracker/
│
├── backend/
│   │
│   ├── manage.py
│   ├── requirements.txt
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   └── attendance/
│       ├── migrations/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       └── permissions.py
│
├── frontend/
│   │
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── hooks/
│       ├── context/
│       ├── App.jsx
│       └── main.jsx
│
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

Make sure you have installed:

* Python 3.x
* Node.js
* npm
* PostgreSQL

---

## 🔧 Backend Setup

Clone the repository:

```bash
git clone https://github.com/your-username/attendance-tracker.git

cd attendance-tracker
```

Move into the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your environment variables:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=attendance_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

JWT_SECRET_KEY=your-jwt-secret
```

Run migrations:

```bash
python manage.py migrate
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Start the backend:

```bash
python manage.py runserver
```

The Django API will be available at:

```text
http://127.0.0.1:8000/
```

---

## Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create the frontend environment file:

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

Start the development server:

```bash
npm run dev
```

The React application will usually be available at:

```text
http://localhost:5173/
```

---

## Authentication

The application uses role-based authentication.

```text
                 ┌─────────────┐
                 │    User     │
                 └──────┬──────┘
                        │
                ┌───────┴───────┐
                ▼               ▼
            Teacher           Student
                │               │
                ▼               ▼
        Manage Sessions    Mark Attendance
        View Records       View Attendance
        View Statistics    View Courses
```

---

## Attendance Model

A typical attendance record contains:

```text
Attendance
├── student
├── course
├── session
├── status
├── marked_at
└── created_at
```

An attendance session can contain:

```text
AttendanceSession
├── course
├── teacher
├── starts_at
├── expires_at
├── qr_token
└── is_active
```

---

## API Overview

Example API endpoints:

### Authentication

```http
POST /api/auth/login/
POST /api/auth/register/
POST /api/auth/refresh/
```

### Courses

```http
GET    /api/courses/
POST   /api/courses/
GET    /api/courses/{id}/
PUT    /api/courses/{id}/
DELETE /api/courses/{id}/
```

### Attendance Sessions

```http
POST /api/attendance/sessions/
GET  /api/attendance/sessions/
GET  /api/attendance/sessions/{id}/
POST /api/attendance/sessions/{id}/close/
```

### Attendance

```http
POST /api/attendance/mark/
GET  /api/attendance/my-attendance/
GET  /api/attendance/course/{id}/
```

> Update these endpoints according to the actual routes implemented in the project.

---

## Security Considerations

The application is designed with several protections against attendance abuse:

* Authentication required before marking attendance
* Server-side validation of QR tokens
* Expiring attendance sessions
* Prevent duplicate attendance
* Role-based permissions
* Environment variables for sensitive configuration
* CSRF/CORS configuration
* Database constraints for attendance records

The QR code is **not treated as proof of identity by itself**. The backend validates the authenticated student and the current attendance session before recording attendance.

---

## Future Improvements

Planned features include:

* [ ] Location-based attendance verification
* [ ] Student attendance percentage warnings
* [ ] Attendance analytics dashboard
* [ ] Export attendance as CSV/PDF
* [ ] Email notifications for low attendance
* [ ] Course timetable integration
* [ ] Teacher dashboard
* [ ] Admin dashboard
* [ ] Attendance reports
* [ ] Multiple departments and semesters
* [ ] Mobile-friendly student interface
* [ ] Deployment with PostgreSQL
* [ ] Automated testing
* [ ] CI/CD with GitHub Actions

---

## Screenshots

Add screenshots of the application here.

### Login

> Add login screenshot

### Teacher Dashboard

> Add teacher dashboard screenshot

### QR Attendance

> Add QR generation screenshot

### Student Dashboard

> Add student dashboard screenshot

### Attendance History

> Add attendance history screenshot

---

## Project Goals

This project was created to explore:

* Building REST APIs with Django REST Framework
* Connecting React with a Django backend
* Authentication and authorization
* Database relationships
* QR-code based workflows
* Time-sensitive authentication tokens
* Attendance management
* Full-stack application architecture

---

## Contributors

* **Your Name** — Backend / Frontend
* **Contributor Name** — Frontend
* **Contributor Name** — Backend

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

Built using:

* Django
* Django REST Framework
* React
* PostgreSQL

For Django documentation and framework references, see the official Django documentation.

If you find this project useful, consider giving the repository a ⭐ on GitHub.
