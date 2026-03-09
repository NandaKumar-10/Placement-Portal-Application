# Placement Portal App — V2

A comprehensive, full-stack **Placement Management System** built with **Vue 3 (Vite)** and **Python/Flask**. This platform seamlessly connects Students, Companies, and University Administrators to streamline the campus recruitment process.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Vue 3, Vite, Vue Router, Bootstrap 5, Chart.js |
| **Backend** | Python, Flask, Flask-SQLAlchemy, JWT |
| **Database** | SQLite |
| **Task Queue & Caching** | Celery, Redis |

---

##  Features

- **Role-Based Access Control** — Secure, JWT-authenticated dashboards for Admins, Companies, and Students.
- **Live Drive Management** — Companies can create job drives, review applicants, and schedule interviews.
- **Student Portals** — Students can upload resumes, browse active placement drives, and apply with a single click.
- **Admin Oversight** — Complete control to approve/reject company registrations, blacklist users, and monitor portal activity.
- **Automated Reporting** — Background tasks (powered by Celery) automatically generate monthly placement statistics.
- **Interactive Analytics** — Real-time data visualization on the Admin dashboard using Chart.js.

---

## Project Structure

```
placement-portal/
│
├── backend/                  # Flask Backend API
│   ├── app.py                # Main application entry point & DB creation
│   ├── model.py              # SQLAlchemy database models
│   ├── auth.py               # Authentication routes (Login/Register)
│   ├── admin.py              # Admin-specific routes
│   ├── company.py            # Company-specific routes
│   ├── student.py            # Student-specific routes
│   ├── tasks.py              # Celery background tasks (e.g., monthly reports)
│   └── requirements.txt      # Python dependencies
│
└── frontend/                 # Vue 3 / Vite Frontend
    ├── index.html            # Main HTML file (contains Chart.js CDN)
    ├── vite.config.js        # Vite bundler configuration
    ├── package.json          # Node.js dependencies
    └── src/
        ├── main.js           # Vue app initialization
        ├── router.js         # Vue Router configuration
        ├── api.js            # Axios configuration for API calls
        ├── App.vue           # Root component
        ├── assets/           # Static images and icons
        └── components/       # Vue views (Admin, Company, Student dashboards)
```

---

## Installation & Setup

### 1. Prerequisites

Ensure the following are installed on your machine:

- Python 3.8+
- Node.js (v16+) & npm
- Redis Server
- Git

---

### 2. Clone the Repository

```bash
git clone https://github.com/23f3001984/Placement-Portal-Application
cd Placement-Portal-Application
```

---

### 3. Backend Setup (Flask API)

```bash
# Create and activate a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

> The backend will run at `http://localhost:5000`.  
> Running `app.py` for the first time will automatically create the SQLite database and a default Admin account.

---

### 4. Frontend Setup (Vue 3 / Vite)

Open a **new terminal** and run:

```bash
cd frontend
npm install
npm run dev
```

> The frontend will run at `http://localhost:5173`.

---

### 5. Background Tasks Setup (Celery & Redis)

To enable automated monthly email reports and background processing:

**Step 1** — Make sure Redis is running.

**Step 2** — Start the Celery Beat scheduler (new terminal, venv activated):

```bash
celery -A tasks:celery_app beat --loglevel=info
```

**Step 3** — Start the Celery Worker (new terminal, venv activated):

```bash
celery -A tasks:celery_app worker --loglevel=info -P solo
```

---

## Default Admin Credentials

When you run `python app.py` for the first time, a master Admin account is created automatically:

| Field | Value |
|---|---|
| **Email** | `admin@placement.com` |
| **Password** | `password` |