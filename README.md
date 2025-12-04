# Blog Management System (Django)

This is a Django Blog Management System that allows users to create, manage, and read blog posts.  
It includes user authentication, categories, search, comments, dashboards, and role-based access.

---

# Features

- User Authentication (Signup / Login / Logout)
- Role Based Access Control (Admin & Author)
- Create, Edit & Delete Blog Posts
- SEO Friendly Slug URLs
- Category Based Filtering
- Keyword Search (Title + Content)
- Comment System
- Pagination
- Image Upload Support
- Admin Dashboard
- Author Dashboard
- Responsive UI using Bootstrap 5

---

# Tech Stack

- Backend: Django 4+
- Frontend: HTML, CSS, Bootstrap 5
- Database: SQLite
- Editor: CKEditor
- Authentication: Django Auth
- Version Control: Git & GitHub

---

# Project Structure

blogproject/
│
├── blog/ # Main app
│ ├── migrations/
│ ├── templates/
│ │ └── blog/
│ ├── static/
│ │ ├── css/
│ │ ├── js/
│ │ └── images/
│ ├── admin.py
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ └── forms.py
│
├── blogproject/ # Project configuration
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── venv/ # Virtual environment
├── manage.py
└── README.md

---

# User Roles

# Admin

- Manage all posts
- Manage all comments
- Full control of the system

# Author (Registered User)

- Create own blog posts
- Edit/Delete only own posts
- Delete comments on own posts

---

# Functionalities Working

- Signup & Login
- Create / Edit / Delete Blog Post
- Category Filtering
- Post Search
- Comment Add & Delete
- Pagination
- Role-based Access Control

# Setup Guide (Installation Steps)

Follow these steps carefully to run the project:

# Create Virtual Environment

```bash
python -m venv venv
#Activate the virtual environment

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the server
python manage.py runserver

# Requirements

Python 3.10+
Django 5.x
Pillow (for image uploads)
Bootstrap 5 (included in static files)
SQLite or any other DB supported by Django

ER Diagram Representation

+-----------+           +-----------+           +-----------+
|   User    |1--------< |   Post    | >--------1| Category  |
+-----------+           +-----------+           +-----------+
| id        |           | id        |           | id        |
| username  |           | title     |           | name      |
| email     |           | slug      |           | slug      |
| password  |           | content   |           +-----------+
+-----------+           | feature_image|
                        | status    |
                        | created_at|
                        | updated_at|
                        | author_id |----+
                        | category_id|    |
                        +-----------+    |
                                         |
                                         v
                                  +-----------+
                                  | Comment   |
                                  +-----------+
                                  | id        |
                                  | body      |
                                  | created_at|
                                  | post_id   |
                                  | user_id   |
                                  +-----------+
Relationships summary:

User → Post = One-to-Many (a user can author multiple posts)
Category → Post = One-to-Many (a category can have multiple posts)
Post → Comment = One-to-Many (a post can have multiple comments)
User → Comment = One-to-Many (a user can make multiple comments)
```
