# Movie Ticketing Application

Welcome to the Movie Ticketing Application repository! This is a monorepo project that provide a robustpython backend for managing movies, cinemas, showtimes, bookings, and user accounts, complemented by a dynamic React frontend for a seamless user experience.

## Table of Contents

---

[Project Overview](#project-overview)

[Features](#features)

[Technologies Used](#technologies-used)

[Prerequisites](#prerequisites)

[Getting Started](#getting-started)

1. [Clone the Repository](#1-clone-the-repository)

2. [Backend Setup (Django)](#backend-django)

2.1. [Navigate to Backend Directory](#21-navigate-to-backend-directory)

2.2. [Set up Python Virtual Environment](#22-set-up-python-virtual-environment)

2.3. [Configure PostgreSQL Database](#23-configure-postgresql-database)

2.4.[Environment Variables (.env)](#24-environment-variables-env)

2.5. [Run Database Migrations](#25-run-database-migrations)

2.6. [Create a Superuser](#26-create-a-superuser)

2.7. [Run the Django Development Server](#27-run-development-server)

2.8. [Backend API Endpoints (Users)](#28-backend-api-endpoints-users)

3. [Frontend Setup (React)](#3-frontend-setup-react)

3.1. [Navigate to Frontend Directory](#31-navigate-to-frontend-directory)

3.2. [Install Node.js Dependencies](#32-install-nodejs-dependencies)

3.3. Run the React Development Server

[Backend-Frontend Communication](#backend-frontend-communication)

[Project Structure](#project-structure)

## Project Overview

This is a full-stack web application for managing movie ticket bookings. The backend is built with Django and Django REST Framework, providing a robust API layer. The frontend is developed using React, consuming these APIs to deliver an interactive user interface.

## Features

### `Backend` (Django)

---

User Authentication & Authorization (Registration, Login, Profile Management)

Custom User Model with `UUIDs` (Universally Unique Identifiers) and a separate Profile model

Secure password handling and JWT-based authentication

Movie Management (CRUD operations)

Cinema & Hall Management (CRUD operations)

Showtime Scheduling

Booking and Seat Reservation Logic

Payment Integration

### `Frontend` (React)

---

User Registration and Login Interface

Movie Listings and Details

Cinema Location Browsing

Showtime Selection and Seat Booking Flow

User Dashboard for Bookings and Profile Management

## Technologies Used

### Backend

---

`Python`: Programming Language (3.10+)

`Django`: Web Framework (latest stable)

`Django REST Framework` (DRF): For building REST APIs

`djangorestframework-simplejwt`: For JWT (JSON Web Token) authentication

`psycopg`: PostgreSQL adapter for Python

`python-decouple`: For managing environment variables

`dj-database-url`: For parsing database URLs from environment variables

`PostgreSQL`: Relational Database

### Frontend

---

`Node.js` (LTS recommended) & `npm`: JavaScript runtime and package manager

`React`: JavaScript library for building user interfaces

`Axios`: For making HTTP requests to the Django API

`React Router`: For client-side routing

`Tailwind CSS` / `Other UI Framework`: For styling

## Development Tools

---

`pipenv`: Python dependency management and virtual environment tool

`Git`: Version Control System

## Prerequisites

---

Before you begin, ensure you have the following installed on your machine:

`Git`: Download & Install Git

`Python 3.10+`: Download & Install Python (Ensure pip is also installed)

`pipenv`: Install globally using pip install pipenv (or python -m pip install pipenv on Windows).ensure you run it as an admin

`Node.js` (LTS recommended): Download & Install Node.js (This includes npm)

`PostgreSQL Database Server`: Download & Install PostgreSQL from [here](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

During installation, remember your superuser password.

After installation, you'll need to create a database and a dedicated user for this project.

## Getting Started

---

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

First, clone the project repository to your local machine:

git clone <https://github.com/ssentongojosh/movie_ticketing_app.git>
cd movie_ticketing_app

---

### 2. Backend Setup (Django)

#### 2.1. Navigate to Backend Directory

```bash
cd backend
```

#### 2.2. Set up Python Virtual Environment

Use `pipenv` to create and activate a virtual environment and install all Python dependencies.

```bash
pipenv shell   # Activates the virtual environment
```

You should see (backend) at the beginning of your terminal prompt, indicating the virtual environment is active.

```bash
pipenv sync   # Installs dependencies from Pipfile.lock, or Pipfile if lock is missing
```

#### 2.3. Configure PostgreSQL Database

You need to create a dedicated database and user for this project in PostgreSQL.

Access PostgreSQL psql shell:

##### On Linux/macOS

```bash
sudo -u postgres psql
```

##### On Windows (if psql is in PATH)

_click start menu and search for pgAdmin and double click to start it_

> create new server. provide the server name under the general tab and the server host as 127.0.0.1 and port as you wish (or go with the default port as 5432) under the connections tab then save

Create Database and User:

> right click the server you have just created and select create --> database and then name the database appropriately

Important: Replace 'your_secure_password_here' with a strong, unique password. Remember this password!

#### 2.4. Environment Variables (.env)

This project uses environment variables for sensitive configurations (like database credentials and secret keys).

Create .env file: Copy the provided example environment file:

```bash
cp .env.example .env
```

or simply copy and paste then modify

Edit .env: Open the newly created .env file and fill in the values:

```bash
# .env file for local development settings

# This file should NOT be committed to version control.

# Create this file from .env.example and fill in your details.

SECRET_KEY=your_django_secret_key_here # Generate a strong, random key (e.g., using Python shell: from django.core.management.utils import get_random_secret_key; print(get_random_secret_key()))
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
TIME_ZONE="Africa/Kampala" # Or your preferred timezone, e.g., America/New_York

# Database URL for PostgreSQL (format: postgres://USER:PASSWORD@HOST:PORT/NAME)

DATABASE_URL=postgres://movie_admin:your_secure_password_here@localhost:5432/movie_ticketing_db

# CORS Allowed Origins for React Development Server

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# CORS_ALLOW_ALL_ORIGINS=False # Uncomment and set to True if you want to allow all origins (less secure for dev)
```

Ensure your_django_secret_key_here and your_secure_password_here are replaced with actual values.

#### 2.5. Run Database Migrations

Apply the database migrations to create the necessary tables in your PostgreSQL database:

```bash
python manage.py migrate
```

#### 2.6. Create a Superuser

Create an administrative user to access the Django admin panel:

```sh
python manage.py createsuperuser
```

Follow the prompts to set up your email and password.

2.7. Run the Django Development Server
Start the Django backend server:

```sh
python manage.py runserver
```

The server will typically run on <http://127.0.0.1:8000/>. You can visit <http://127.0.0.1:8000/admin/> to log into the Django administration site with your superuser credentials.

#### 2.8. Backend API Endpoints (Users)

The following core user authentication endpoints are available:

`POST /api/v1/users/register/`: Register a new user.

```json
Body: {"email": "...", "phone_number": "...", "password": "...", "password2": "..."}
```

`POST /api/v1/users/login/`: Log in and obtain JWT access and refresh tokens.

```json
Body: {"email": "...", "password": "..."}
```

`POST /api/v1/users/token/refresh/`: Refresh an expired access token using a refresh token.

```json
Body: {"refresh": "..."}
```

`GET /api/v1/users/profile/`: Retrieve the authenticated user's profile.

```http
Headers: Authorization: Bearer <access_token>
```

`PUT/PATCH /api/v1/users/profile/`: Update the authenticated user's profile.

```http
Headers: Authorization: Bearer <access_token>

Body: {"full_name": "...", "location_preferences": "...", ...}
```
#### 2.7 Run Development Server
```bash
python manage.py runserver
```

### 3. Frontend Setup (React)

This section details how to set up and run the React frontend application.

#### 3.1. Navigate to Frontend Directory

Open a new terminal window and navigate to the frontend directory (from the project root):

```bash
cd frontend
```

#### 3.2. Install Node.js Dependencies

Use npm (Node Package Manager) or yarn to install all necessary JavaScript dependencies for the React app:

```bash
npm install
```

The frontend application will typically open in your browser at <http://localhost:3000/>.

## Backend-Frontend Communication

The React frontend communicates with the Django backend via RESTful API calls. Here's how the connection is established and managed:

> `API Endpoints`: The Django backend exposes its functionalities through a set of REST API endpoints (e.g., /`api/v1/users/register/`, `/api/v1/users/login/`). The frontend will make HTTP requests (GET, POST, PUT, DELETE) to these URLs.

## CORS (Cross-Origin Resource Sharing)

During development, your React app runs on <http://localhost:3000> and your Django backend on <http://127.0.0.1:8000>. These are considered different "origins" by web browsers.

To allow your frontend to make requests to your backend, Django is configured with django-cors-headers.

The CORS_ALLOWED_ORIGINS setting in backend/movie_ticketing_project/settings/development.py explicitly lists <http://localhost:3000> and <http://127.0.0.1:3000> as allowed origins. This prevents CORS errors in your browser.

HTTP Client (Axios):

The React frontend will use a library like Axios to send HTTP requests to the Django API.

Example (in a React component):

```javascript
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api/v1"; // Or 'http://localhost:8000/api/v1'

// Example: User login
const loginUser = async (email, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/users/login/`, {
      email,
      password,
    });
    console.log("Login successful:", response.data);
    // Store tokens (e.g., in localStorage or context)
    localStorage.setItem("access_token", response.data.access);
    localStorage.setItem("refresh_token", response.data.refresh);
    return response.data;
  } catch (error) {
    console.error("Login failed:", error.response.data);
    throw error;
  }
};

// Example: Fetch user profile (requires authentication)
const fetchUserProfile = async () => {
  try {
    const accessToken = localStorage.getItem("access_token");
    const response = await axios.get(`${API_BASE_URL}/users/profile/`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    console.log("User profile:", response.data);
    return response.data;
  } catch (error) {
    console.error("Failed to fetch profile:", error.response.data);
    throw error;
  }
};
```

## JWT Authentication

Upon successful login or registration, the Django backend sends back JWT access and refresh tokens.

The frontend should store these tokens securely (e.g., in localStorage or sessionStorage for development, more securely in production).

For subsequent authenticated requests (like fetching a user profile), the access token must be included in the Authorization header as Bearer <access_token>.

If the access token expires, the frontend can use the refresh token to obtain a new access token without requiring the user to log in again.

## Project Structure

```plaintext
movie_ticketing_app/
├── backend/ # Django backend project
│ ├── MovieTicketingProject/ # Main Django project configuration
│ │ ├── settings/ # Modular Django settings (base, development, production)
│ │ └── urls.py # Main URL dispatcher
│ ├── users/ # Django app for user authentication and management
│ │ ├── models.py # Custom User model definitions
│ │ ├── serializers.py # DRF serializers for user data
│ │ ├── views.py # API views for user endpoints
│ │ ├── urls.py # URL patterns for user APIs
│ │ └── signals.py # Django signals (e.g., auto-create profile)
│ ├── profile/ # Django app for user profile details (one-to-one with CustomUser)
│ │ ├── models.py # Profile model definition
│ │ └── ...
│ ├── Pipfile # Pipenv dependency definitions
│ ├── Pipfile.lock # Locked Python dependencies
│ ├── .env.example # Template for environment variables
│ ├── .env # Local environment variables (NOT committed to Git)
│ └── manage.py # Django's command-line utility
├── frontend/ # React frontend project
│ ├── node_modules/ # Node.js dependencies
│ ├── public/ # Static assets (index.html, favicon, etc.)
│ ├── src/ # React components, logic, styles
│ │ ├── components/ # Reusable UI components
│ │ ├── pages/ # Top-level components for different views/routes
│ │ ├── services/ # API interaction logic (e.g., auth.js, user.js)
│ │ ├── App.js # Main application component
│ │ ├── index.js # React app entry point
│ │ └── ...
│ ├── package.json # Node.js project configuration
│ ├── README.md # Frontend-specific README (optional, can be merged into main)
│ └── yarn.lock (or package-lock.json) # Locked Node.js dependencies
└── README.md # Project-wide README (this file)
```
