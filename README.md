<div align="center">

# Blogicum

<em>A platform for publishing posts and sharing thoughts</em>

<br>

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat-square&logo=sqlite&logoColor=white)

<br>

<a href="https://github.com/Samos006/Blogicum"><strong>📦 GitHub Repository</strong></a>

</div>

---

## Table of Contents

- [About](#about)
- [Key Features](#key-features)
- [Technical Details](#technical-details)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [Status](#status)

---

## About

**Blogicum** is a minimalist blogging platform where anyone can maintain their own diary, publish posts, and share stories. The project is built for those who value simplicity in content creation and want to join a community of authors.

---

## Key Features

| | |
|---|---|
| **📝 Post Management**<br>Create, edit, and delete entries | **👥 Authors & Readers**<br>View author profiles and publication feeds |
| **🏷️ Categories**<br>Group posts by topics for easy navigation | **💬 Commenting**<br>Discuss posts with other readers |
| **🔐 Authentication**<br>Registration and login for authors | **📱 Responsive Design**<br>Comfortable reading on any device |

---

## Technical Details

<details>
<summary><strong>🏗️ Architecture</strong></summary>
<br>

- **MVT Pattern** — classic Django architecture with separated logic
- **CBV (Class-Based Views)** — reusable class-based views
- **Templates** — inheritance and component reuse

</details>

<details>
<summary><strong>🗄️ Database</strong></summary>
<br>

- **SQLite** — for development and small projects
- **Migrations** — database schema management via Django ORM

</details>

<details>
<summary><strong>🔒 Security</strong></summary>
<br>

- **CSRF Protection** — built-in Django mechanisms
- **XSS Protection** — automatic escaping in templates
- **Authentication** — standard Django user system

</details>

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Samos006/Blogicum.git
cd Blogicum


# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (optional - for custom settings)
cat > .env << EOF
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EOF

# Apply migrations
python manage.py migrate

# Create superuser (optional - skip by pressing Enter)
python manage.py createsuperuser

# Load demo data (optional)
python manage.py loaddata demo_data.json

# Run development server
python manage.py runserver
