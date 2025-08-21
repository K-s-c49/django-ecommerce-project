🛒 Django E-Commerce Project

A fully functional E-commerce Web Application built with Django, featuring authentication, product management, shopping cart, wishlist, address management, and Razorpay Payment Gateway integration.

🚀 Features
🔐 User Authentication (Register, Login, Logout, Profile)
🛍 Product Management (Browse products category-wise)
🛒 Shopping Cart (Add, update, remove items)
❤️ Wishlist (Save favorite products)
🏠 Address Management (Add multiple delivery addresses)
💳 Razorpay Payment Integration (Secure online payments)
📦 Order Management (Checkout and order placement)

🛠️ Tech Stack
Backend: Django (Python)
Frontend: HTML, CSS, JavaScript, Bootstrap
Database: SQLite (default) / can be switched to PostgreSQL/MySQL
Payment Gateway: Razorpay

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/django-ecommerce-project.git
cd django-ecommerce-project

2️⃣ Create Virtual Environment
python -m venv venv

Activate the environment:
venv\Scripts\activate

Windows (PowerShell):
.\venv\Scripts\Activate


macOS/Linux:
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Setup Database
Run migrations:
python manage.py migrate

5️⃣ Create Superuser (Admin Access)
python manage.py createsuperuser

6️⃣ Run Development Server
python manage.py runserver

