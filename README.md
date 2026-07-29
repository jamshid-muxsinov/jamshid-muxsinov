<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="Backend Python Developer Portfolio — Django, FastAPI, aiogram">
</p>

---

## About Me

Backend Python developer with 2+ years of experience building production-ready systems. I design REST APIs, real-time applications, Telegram bots, and full-stack solutions with **Django**, **FastAPI**, and **aiogram**. Comfortable with PostgreSQL, Redis, Celery, Docker, WebSockets, and deployment pipelines.

---

<p align="center">
  <img src="./assets/readme/section-django.svg" width="100%" alt="Django Projects section header">
</p>

### DocWeave — Markdown Document Platform

A lightweight Django Markdown document platform with real-time collaboration foundations. CRUD documents, sharing with roles (owner/editor/viewer), Markdown rendering with sanitization, version history, image uploads, and WebSocket-based presence/typing/draft sync.

<p align="center">
  <img src="./assets/readme/badge-django.svg" alt="Django">
  <img src="./assets/readme/badge-postgresql.svg" alt="PostgreSQL">
  <img src="./assets/readme/badge-redis.svg" alt="Redis">
  <img src="./assets/readme/badge-channels.svg" alt="Channels">
  <img src="./assets/readme/badge-docker.svg" alt="Docker">
</p>

**Key features:**
- Auth system with registration/login
- Document dashboard with CRUD, search, and filtering
- Sharing management with role-based access (owner/editor/viewer)
- Version history with restore and export (.md/.html)
- WebSocket `/ws/docs/<document_id>/` — real-time presence, typing indicators, draft sync
- Markdown sanitization (bleach), image uploads, live preview
- 97 Django tests

---

### Logistics Tracking (kurs) — Full-Stack Cargo System

A logistics/cargo tracking system with Django web app, public site (blog), admin panel, Telegram bot for cargo tracking, WebSocket consumers for real-time updates, Celery for background tasks, and Google Sheets integration.

<p align="center">
  <img src="./assets/readme/badge-django.svg" alt="Django">
  <img src="./assets/readme/badge-drf.svg" alt="DRF">
  <img src="./assets/readme/badge-postgresql.svg" alt="PostgreSQL">
  <img src="./assets/readme/badge-redis.svg" alt="Redis">
  <img src="./assets/readme/badge-celery.svg" alt="Celery">
  <img src="./assets/readme/badge-channels.svg" alt="Channels">
  <img src="./assets/readme/badge-docker.svg" alt="Docker">
</p>

**Key features:**
- Django + DRF backend with Product, StaffProfile, InviteCode models
- Public blog site
- `bot_tracking.py` — aiogram Telegram bot for cargo status tracking
- WebSocket consumers for real-time status updates
- Celery + django-celery-beat for background tasks
- Google Sheets integration (gspread), Excel export (openpyxl/pandas)
- Docker + Nginx deployment

---

### Burgut Logistics (sa_kurs) — Defense Version

A logistics and cargo delivery management system with public site, admin panel, Telegram bot, delivery calculator, cargo tracking, Google Forms webhooks, and Excel export. Includes i18n (Russian, Uzbek, English).

<p align="center">
  <img src="./assets/readme/badge-django.svg" alt="Django">
  <img src="./assets/readme/badge-drf.svg" alt="DRF">
  <img src="./assets/readme/badge-postgresql.svg" alt="PostgreSQL">
  <img src="./assets/readme/badge-redis.svg" alt="Redis">
  <img src="./assets/readme/badge-celery.svg" alt="Celery">
  <img src="./assets/readme/badge-channels.svg" alt="Channels">
  <img src="./assets/readme/badge-docker.svg" alt="Docker">
</p>

**Key features:**
- Django + DRF with Product, StaffProfile, InviteCode, Cargo models
- Delivery calculator (avia, auto, rail, sea)
- Google Forms webhook integration
- Telegram bot for tracking
- i18n: Russian, Uzbek, English
- Excel export with openpyxl/pandas

---

<p align="center">
  <img src="./assets/readme/section-fastapi.svg" width="100%" alt="FastAPI Projects section header">
</p>

### AutoWash Pass — Car Wash Subscription System

Full-stack car wash subscription system with FastAPI backend, Kotlin Jetpack Compose Android client + terminal kiosk app, and Astro admin dashboard. Covers user registration, subscription plans, QR code generation, terminal scanning, wash session timer, payments, and ratings.

<p align="center">
  <img src="./assets/readme/badge-fastapi.svg" alt="FastAPI">
  <img src="./assets/readme/badge-sqlalchemy.svg" alt="SQLAlchemy">
  <img src="./assets/readme/badge-alembic.svg" alt="Alembic">
  <img src="./assets/readme/badge-postgresql.svg" alt="PostgreSQL">
  <img src="./assets/readme/badge-firebase.svg" alt="Firebase">
</p>

**Key features:**
- API routers: `/auth`, `/users`, `/plans`, `/subscriptions`, `/payments`, `/sessions`, `/terminal`, `/car-washes`, `/devices`
- QR code generation and terminal scanning
- Wash session timer with real-time status
- Firebase push notifications
- APScheduler for background jobs, SSE for real-time updates
- PyJWT + bcrypt auth
- 81 pytest tests

---

### WeConstruct CRM — Construction Company CRM

A construction company CRM with two apps: admin panel (Kanban board, project management) and public website (shop). Bilingual (ru/uz), with caching, rate limiting, CSRF protection, and Google Sheets integration.

<p align="center">
  <img src="./assets/readme/badge-fastapi.svg" alt="FastAPI">
  <img src="./assets/readme/badge-sqlalchemy.svg" alt="SQLAlchemy">
  <img src="./assets/readme/badge-alembic.svg" alt="Alembic">
  <img src="./assets/readme/badge-postgresql.svg" alt="PostgreSQL">
  <img src="./assets/readme/badge-redis.svg" alt="Redis">
  <img src="./assets/readme/badge-docker.svg" alt="Docker">
</p>

**Key features:**
- Admin app: Kanban board, CRUD, protected routes, locale routing (`/{locale}/...`)
- Site app: public website with shop, sitemap.xml, robots.txt
- HTMX integration for interactive UI
- CacheMiddleware + RateLimitMiddleware
- Webhooks, API routes, SSE
- starlette-wtf (CSRF), fastapi-pagination
- Google Sheets integration (gspread)
- Docker + Nginx deployment

---

### AI Photo Studio — AI Marketing Photo Generator

An AI-powered marketing photo generator for clothing. Upload a garment photo, choose background/angle, and AI generates professional model photos for marketplaces. React 18 + TypeScript frontend with FastAPI backend.

<p align="center">
  <img src="./assets/readme/badge-fastapi.svg" alt="FastAPI">
  <img src="./assets/readme/badge-sqlalchemy.svg" alt="SQLAlchemy">
  <img src="./assets/readme/badge-alembic.svg" alt="Alembic">
  <img src="./assets/readme/badge-postgresql.svg" alt="PostgreSQL">
  <img src="./assets/readme/badge-redis.svg" alt="Redis">
  <img src="./assets/readme/badge-minio.svg" alt="MinIO">
  <img src="./assets/readme/badge-docker.svg" alt="Docker">
</p>

**Key features:**
- JWT auth: `POST /api/auth/register`, `/api/auth/login`
- Generation pipeline: `POST /api/generations/` (upload + params)
- Gallery: `GET /api/generations/`, `GET /api/generations/{id}`
- WebSocket `/ws/status/{user_id}` — real-time generation status
- HuggingFace Inference API (FLUX.1-schnell), Google Gemini
- MinIO (S3) for object storage, boto3, Pillow
- React 18 + TypeScript + Tailwind CSS + Vite frontend
- Zustand state management, Axios

---

### Logistics Chat Simulator (v1) — Educational Platform

An educational platform where students practice logistics scenarios via simulated chat conversations with AI characters (driver, client, warehouse worker). Teachers can monitor and intervene.

<p align="center">
  <img src="./assets/readme/badge-fastapi.svg" alt="FastAPI">
  <img src="./assets/readme/badge-sqlalchemy.svg" alt="SQLAlchemy">
  <img src="./assets/readme/badge-socketio.svg" alt="Socket.IO">
  <img src="./assets/readme/badge-alembic.svg" alt="Alembic">
</p>

**Key features:**
- Routers: auth, characters, chats, messages, cases, students, teachers, templates, groups, takeover, upload
- Socket.IO events: `send:message`, `join:chat`, `typing:start/stop`, `student:need_help`, `teacher:resolve_help`
- Case system with branching decisions and scoring
- Teacher takeover mode
- Student groups, profiles, progress tracking
- Markdown case import from files
- structlog, slowapi (rate limiting)

---

### Cargo Tracker Admin Panel & Bot

A logistics cargo tracking system with a FastAPI admin panel and Telegram bot. Clients track packages by phone number; admins manage clients, warehouses, trucks, products, status templates via web UI.

<p align="center">
  <img src="./assets/readme/badge-fastapi.svg" alt="FastAPI">
  <img src="./assets/readme/badge-aiogram.svg" alt="aiogram">
  <img src="./assets/readme/badge-sqlalchemy.svg" alt="SQLAlchemy">
  <img src="./assets/readme/badge-alembic.svg" alt="Alembic">
  <img src="./assets/readme/badge-postgresql.svg" alt="PostgreSQL">
</p>

**Key features:**
- Telegram bot: `/start`, my cargo list, phone binding, status history (ru/uz bilingual)
- Admin panel at `/admin/*`: client, warehouse, truck, product, status template management
- Models: Client, Warehouse, Truck, Product, StatusTemplate, StatusUpdate, User, AdminUser, InviteCode
- FSM states for phone number input
- aiogram SessionMiddleware, bcrypt

---

### Consultation Forwarder — Website to Telegram

A minimal FastAPI endpoint that receives form data (name, phone, message) from a website and forwards it as a formatted Telegram message to configured recipients. Includes a claim-leaderboard button handler.

<p align="center">
  <img src="./assets/readme/badge-fastapi.svg" alt="FastAPI">
  <img src="./assets/readme/badge-aiogram.svg" alt="aiogram">
</p>

**Key features:**
- `POST /api_new_request` — receive consultation form, forward to Telegram
- `claim_lead` callback — inline button for staff to claim a lead
- Static file serving
- Minimal: FastAPI + aiogram in one file, no database

---

### FastAPI To-Do API — Study Project

A small FastAPI To-Do CRUD study project. In-memory "database" (dict), 7 endpoints for task management.

<p align="center">
  <img src="./assets/readme/badge-fastapi.svg" alt="FastAPI">
</p>

**Key features:**
- `POST /tasks` — create
- `GET /tasks` — list all
- `GET /tasks/{id}` — get one
- `PUT /tasks/{id}` — update
- `DELETE /tasks/{id}` — delete
- `POST /tasks/{id}/complete` — mark done
- `GET /tasks/pending` — pending tasks

---

<p align="center">
  <img src="./assets/readme/section-aiogram.svg" width="100%" alt="Telegram Bots section header">
</p>

### Telegram Video Downloader Bot

Accepts video URLs, downloads via yt-dlp, sends video files back through Telegram. Supports YouTube, Instagram, TikTok, Twitter/X, and 1000+ sites.

<p align="center">
  <img src="./assets/readme/badge-aiogram.svg" alt="aiogram">
</p>

**Key features:**
- `/start`, `/help` commands
- URL detection and video download via yt-dlp
- Progress status updates
- Error handling for large files, private videos, anti-bot, timeouts
- Cookie/proxy support for YouTube
- Configurable JS runtime (node/deno)

---

## Tech Stack Summary

| Category | Technologies |
|----------|-------------|
| **Languages** | Python 3.10+, SQL |
| **Frameworks** | Django 4.x, Django REST Framework, FastAPI, aiogram 3 |
| **Databases** | PostgreSQL, SQLite, Redis |
| **ORMs** | Django ORM, SQLAlchemy (async), Alembic |
| **Async** | asyncio, WebSockets, Socket.IO, SSE, Celery |
| **Infrastructure** | Docker, Nginx, Gunicorn, Daphne |
| **Integrations** | Telegram Bot API, Firebase, Google Sheets, MinIO (S3), HuggingFace |
| **Testing** | pytest, Django TestCase |

---

<p align="center">
  <sub>Backend Python Developer Portfolio — Built with Django, FastAPI & aiogram</sub>
</p>
