

Django Custom User Authentication API

This project implements a custom user model in Django with Django REST Framework (DRF) for user registration, login, and token-based authentication. It uses rest_framework.authtoken to generate and manage authentication tokens.

🚀 Features

Custom User model extending Django’s AbstractUser

User registration with profile fields (bio, location, date of birth, profile picture)

Secure password hashing

Token-based authentication

Login endpoint that returns a token

DRF serializers for user creation and authentication

⚙️ Setup Instructions
1. Clone the repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Apply migrations
python manage.py makemigrations
python manage.py migrate

5. Create a superuser (for admin access)
python manage.py createsuperuser

6. Run the server
python manage.py runserver


API will be available at: http://127.0.0.1:8000/

🧑‍💻 User Model Overview

The custom user model extends AbstractUser and includes:

Field	Type	Notes
email	Email	Used as the username field (unique)
first_name	String	Optional
last_name	String	Optional
date_of_birth	Date	Optional
bio	Text	Optional user bio
location	String	Optional location
profile_picture	Image	Optional profile photo
password	String	Hashed automatically

AUTH_USER_MODEL in settings.py points to this custom model.

🔑 Authentication

This project uses Token Authentication. After registering or logging in, a token is returned. You must include this token in the Authorization header for authenticated requests.

Header format:

Authorization: Token <your_token_here>

📌 API Endpoints
1. Register a New User

POST /api/register/

Request Body:

{
  "email": "user@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-01",
  "bio": "Hello, I'm John!",
  "location": "Accra",
  "profile_picture": null
}


Response:

{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-01",
  "bio": "Hello, I'm John!",
  "location": "Accra",
  "profile_picture": null,
  "token": "2f3a61c3bda84c9a9caa47e20a..."
}

2. Login User

POST /api/login/

Request Body:

{
  "email": "user@example.com",
  "password": "securepassword123"
}


Response:

{
  "token": "2f3a61c3bda84c9a9caa47e20a..."
}

3. Access Protected Endpoint

Include your token in the request header:

Authorization: Token 2f3a61c3bda84c9a9caa47e20a...
