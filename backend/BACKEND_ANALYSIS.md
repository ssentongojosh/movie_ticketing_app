# Backend Analysis: Movie Ticketing App

This document provides a comprehensive overview of the backend architecture, technologies, and functionality for the Movie Ticketing App.

## 🚀 Technology Stack

- **Framework:** [Django](https://www.djangoproject.com/) (Python)
- **API Framework:** [Django REST Framework (DRF)](https://www.django-rest-framework.org/)
- **Authentication:** [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) (JSON Web Tokens)
- **Database:** PostgreSQL (via `psycopg` and `dj-database-url`)
- **Configuration:** [python-decouple](https://github.com/HBNetwork/python-decouple) for environment variables.
- **Environment Management:** Pipenv (`Pipfile`)

## 📁 Project Structure

```text
backend/
├── MovieTicketingProject/      # Project configuration
│   ├── settings/               # Split settings (base, development)
│   ├── templates/              # Email templates (verification, password reset)
│   ├── urls.py                 # Main URL routing
│   └── ...
├── users/                      # User management & Authentication app
│   ├── models.py               # CustomUser model
│   ├── serializers.py          # Data validation & serialization
│   ├── views.py                # API Logic
│   └── urls.py                 # User-specific routing
├── userprofile/                # Extended user information app
│   ├── models.py               # UserProfile model
│   └── ...
├── manage.py                   # Django management script
└── Pipfile                     # Dependency management
```

## 🔐 Authentication & User Management

### Custom User Model (`users.CustomUser`)
The project uses a custom user model instead of the default Django User.
- **Identifier:** `email` (unique)
- **Primary Key:** `UUID` for enhanced security and scalability.
- **Fields:** `phone_number`, `is_verified`, `is_admin`, `status`, etc.
- **Social Auth Readiness:** Already contains `provider` and `provider_id` fields for future OAuth integration.
- **Manager:** `CustomUserManager` handles user and superuser creation.

### JWT Authentication
- **Login:** Returns `access` and `refresh` tokens.
- **Security:** Standard DRF permission classes (`IsAuthenticated`, `AllowAny`) are used to protect endpoints.

### Email Workflows
- **Email Verification:** Users receive a verification link upon registration or request.
- **Password Reset:** Secure token-based password reset workflow.
- **Templates:** HTML and Text templates for emails are located in `MovieTicketingProject/templates/`.

## 🌟 Future Enhancement: Google Login

The application is architecturally prepared for social authentication, though the logic is currently pending.

### Recommended Implementation
The easiest and most robust path is using **`dj-rest-auth`** with **`django-allauth`**.

**1. Dependencies:**
```bash
pipenv install dj-rest-auth django-allauth
```

**2. Configuration Steps:**
- Add `allauth`, `allauth.account`, `allauth.socialaccount`, and `allauth.socialaccount.providers.google` to `INSTALLED_APPS`.
- Configure `AUTHENTICATION_BACKENDS` in `settings/base.py`.
- Register the Google Client ID and Secret in the Django Admin portal.

**3. Integration Flow:**
- The frontend (React) obtains a Google ID/Access Token.
- The token is sent to a backend view (provided by `dj-rest-auth`).
- The backend validates the token with Google, creates or updates the `CustomUser` (setting `provider='google'`), and returns a standard JWT `access`/`refresh` pair.

## 🛠️ Applications

### 1. `users` App
Responsible for the core identity and security of the application.
- **Key Files:**
    - `email_verification_serializers.py`: Handles verification token logic.
    - `password_reset_serializers.py`: Handles password reset token logic.
    - `signals.py`: (Likely) handles automatic profile creation.

### 2. `userprofile` App
Extends the `CustomUser` model with additional personal details.
- **UserProfile Model:** Linked 1:1 with `CustomUser`.
- **Fields:** `full_name`, `location_preferences`, `notification_preferences` (JSON), `payment_methods` (JSON).

## 🛣️ API Endpoints (v1)

Base URL: `/api/v1/users/`

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `register/` | POST | Register a new user account. |
| `login/` | POST | Obtain JWT access/refresh tokens. |
| `token/refresh/` | POST | Refresh an expired access token. |
| `profile` | GET/PATCH | Get or Update current user profile. |
| `password-reset/request/` | POST | Request a password reset email. |
| `password-reset/confirm/` | POST | Confirm password reset with token. |
| `email-verification/request/` | POST | Request a new verification email. |
| `email-verification/confirm/` | POST | Confirm email verification with token. |

## ⚙️ Configuration

Settings are split for modularity:
- **`base.py`:** Common settings (Apps, Middleware, Templates, Auth).
- **`development.py`:** Local settings (DEBUG=True, CORS, Console Email Backend).

### Key Environment Variables (`.env`)
- `SECRET_KEY`: Django secret key.
- `DEBUG`: Boolean flag for debug mode.
- `DATABASE_URL`: Connection string for the database.
- `ALLOWED_HOSTS`: List of allowed hostnames.
- `CORS_ALLOWED_ORIGINS`: Allowed origins for cross-origin requests (e.g., React frontend).

## 🧪 Development Workflow

1. **Install Dependencies:** `pipenv install`
2. **Migrations:** `python manage.py migrate`
3. **Run Server:** `python manage.py runserver`
4. **Emails:** In development, emails are printed to the terminal console.
