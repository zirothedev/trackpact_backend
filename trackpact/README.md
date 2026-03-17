# TrackPact — Workout Accountability App

A simple Django MVP that helps users stay consistent with workouts
using an accountability partner.

---

## Setup (takes ~2 minutes)

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 2. Install Django
pip install -r requirements.txt

# 3. Run database migrations (creates db.sqlite3 automatically)
python manage.py migrate

# 4. Create an admin account (optional but useful)
python manage.py createsuperuser

# 5. Start the server
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## Project Structure

```
trackpact/
├── trackpact/          # Project config (settings, urls, wsgi)
├── accounts/           # Register, login, logout, profile
├── workouts/           # Workout logging, dashboard
│   └── management/
│       └── commands/
│           └── check_missed_workouts.py   # Daily check command
├── partners/           # Partner invites, reminders
├── manage.py
└── requirements.txt
```

---

## Daily Missed Workout Check

Run this command once a day (e.g. via cron at 11pm):

```bash
python manage.py check_missed_workouts
```

It checks every user who has a partner. If they didn't log a workout
today, it emails their partner automatically.

**Cron example (runs at 11pm every day):**
```
0 23 * * * /path/to/venv/bin/python /path/to/manage.py check_missed_workouts
```

---

## Email Setup

By default, emails are printed to the terminal (no SMTP needed for dev).

To send real emails, edit `trackpact/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'you@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

---

## URL Map

| URL                        | What it does                  |
|----------------------------|-------------------------------|
| `/`                        | Landing page                  |
| `/accounts/register/`      | Sign up                       |
| `/accounts/login/`         | Log in                        |
| `/accounts/logout/`        | Log out                       |
| `/accounts/profile/`       | Edit profile / fitness goal   |
| `/dashboard/`              | View workouts + stats         |
| `/workouts/add/`           | Log a workout                 |
| `/workouts/`               | Full workout history           |
| `/partners/`               | Partner status page           |
| `/partners/invite/`        | Send a partner invite         |
| `/partners/remind/`        | Send reminder to partner      |
| `/admin/`                  | Django admin panel            |

---

## Apps Overview

### `accounts`
- `UserProfile` model — extends User with `fitness_goal` and `partner`
- Register view creates a User + UserProfile together
- Login/logout use Django's built-in auth views

### `workouts`
- `Workout` model — title, duration, date, notes
- Dashboard shows last 10 workouts + today's status
- Management command checks for missed workouts daily

### `partners`
- `PartnerRequest` model — tracks invite status (pending/accepted/declined)
- Invite by email → receiver accepts → both profiles linked
- Manual reminder sends a custom email to your partner
