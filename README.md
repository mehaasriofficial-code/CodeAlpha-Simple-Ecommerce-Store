# CodeAlpha - Simple E-commerce Store

A beginner-friendly full-stack e-commerce project for the CodeAlpha internship task.

## Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Django (Python)
- Database: SQLite
- Authentication: Django built-in user authentication
- Cart: Session-based cart

## Features
- Product listing
- Product details
- Add/remove/update shopping cart
- User registration and login/logout
- Checkout and order processing
- Orders stored in SQLite database
- Admin panel for products and orders
- Responsive student-friendly UI

## Run the project

### 1. Install Python
Python 3.10+ is recommended.

### 2. Create virtual environment
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install packages
```bash
pip install -r requirements.txt
```

### 4. Create database
```bash
python manage.py migrate
```

### 5. Add sample products
```bash
python manage.py seed_products
```

### 6. Start server
```bash
python manage.py runserver
```

Open:
http://127.0.0.1:8000/

Admin:
http://127.0.0.1:8000/admin/

Create an admin user:
```bash
python manage.py createsuperuser
```

## Important
The SQLite database file is created after `migrate`. Products can be added through the admin panel or the seed command.
