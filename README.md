# SaaS PM App

A full-stack multi-tenant project management SaaS application.

## Tech Stack
**Backend:** Django · Django REST Framework · JWT · PostgreSQL · drf-spectacular  
**Frontend:** React 19 · Vite · TailwindCSS *(in progress)*

## Features
- JWT Authentication (register, login, token refresh)
- Multi-tenant Organizations with Role-Based Access Control
- Project management per organization
- Task management with priority, status, assignee, due date
- Auto-generated Swagger API docs at `/api/docs/`

## API Endpoints
| Resource | Endpoints |
|----------|-----------|
| Auth | `/api/auth/register/` `/api/auth/login/` `/api/auth/me/` |
| Organizations | `/api/organizations/` `/api/organizations/{id}/members/` |
| Projects | `/api/projects/` `/api/projects/{id}/` |
| Tasks | `/api/tasks/` `/api/tasks/{id}/` |

## Local Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API docs: `http://127.0.0.1:8000/api/docs/`