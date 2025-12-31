live demo https://khushalsingh.pythonanywhere.com/

🛒 Django E-Commerce Project

A complete E-commerce web application built with Django, designed to provide a smooth shopping experience.
The project comes with user authentication, product browsing by categories, cart & wishlist functionality, address management, and Razorpay payment gateway integration.

🚀 Features

🔐 User Authentication – Register, Login, Logout, and Profile Management
🛍 Product Management – Browse products by categories
🛒 Shopping Cart – Add, update, and remove items with ease
❤️ Wishlist – Save products for later
🏠 Address Management – Add and manage multiple delivery addresses
💳 Razorpay Payment Gateway – Secure online payments
📦 Order Management – Smooth checkout and order tracking

🛠️ Tech Stack

Backend: Django (Python)
Frontend: HTML, CSS, JavaScript, Bootstrap
Database: SQLite (default) → can be switched to PostgreSQL/MySQL
Payment Gateway: Razorpay

⚙️ Installation & Setup

Follow the steps below to set up the project on your local machine.

1️⃣ Clone the Repository
git clone https://github.com/K-s-c49/django-ecommerce-project.git
cd django-ecommerce-project

2️⃣ Create a Virtual Environment
python -m venv venv


Activate the environment:

Windows (CMD):

venv\Scripts\activate


Windows (PowerShell):

.\venv\Scripts\Activate


macOS/Linux:

source venv/bin/activate

3️⃣ Install Dependencies

For the first setup, install these essentials:

pip install django
pip install razorpay  
pip install --upgrade setuptools  
pip install wheel  
pip install Pillow


If you already have a requirements.txt file, simply run:
pip install -r requirements.txt

4️⃣ Setup the Database

Run migrations:
* python manage.py migrate

5️⃣ Create a Superuser (Admin Access)
python manage.py createsuperuser

6️⃣ Run the Development Server
python manage.py runserver

(optional)
💳 Razorpay Payment Setup
To enable online payments, you need to configure Razorpay:
* Create an account at Razorpay
* Go to the Dashboard → API Keys section.
* Generate a new Key ID and Key Secret.

Open your settings.py file and add the keys:

# Razorpay Configuration
1.RAZORPAY_KEY_ID = "your_key_id"
2.RAZORPAY_KEY_SECRET = "your_secret_key"

In your checkout or payment view, use these keys to integrate Razorpay’s order API.
Make sure to use test mode keys while developing, and live keys when deploying.
etc..
