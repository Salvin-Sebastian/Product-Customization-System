# High-Performance Product Customization System

A modern, fast, and reliable web application built with Django that allows users to upload their own designs (logos, art) and realistically preview them on various products (like T-Shirts, mugs, etc.) from different angles.

## ✨ Features

* **Realistic Image Mapping:** Automatically removes backgrounds from uploaded designs, resizes them, and realistically warps and blends them onto the product to match the perspective and fabric curves.
* **Background Processing:** Heavy image processing tasks are offloaded to **Celery** and **Redis** to ensure the web interface remains lightning-fast and non-blocking.
* **Modern UI/UX:** A premium, glassmorphism-inspired frontend interface built with raw HTML/CSS/JS for a wow-factor user experience.
* **Dynamic Status Polling:** The frontend automatically polls the backend for rendering status and seamlessly updates the UI without page reloads.
* **Admin Dashboard:** Fully integrated Django Admin panel to manage Products, Product Views (Front, Back, Side), and configure exact print area coordinates.

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Image Processing:** OpenCV, Pillow, Numpy
* **Task Queue:** Celery, Redis
* **Frontend:** HTML5, CSS3 (Modern, Vanilla), JavaScript (Fetch API)
* **Database:** SQLite (Default, configurable)

## 📋 Prerequisites

Before running the project locally, ensure you have the following installed:
* **Python 3.8+**
* **Redis:** The Celery message broker. 
  * *Windows:* You can use [Memurai](https://www.memurai.com/) or run Redis via Docker (`docker run -d -p 6379:6379 redis`).
  * *Mac/Linux:* `brew install redis` or `sudo apt install redis-server`.

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Salvin-Sebastian/Product-Customization-System.git
   cd Product-Customization-System
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations**
   ```bash
   python manage.py makemigrations customizer
   python manage.py migrate
   ```

5. **Create a Superuser (for Admin access)**
   ```bash
   python manage.py createsuperuser
   ```

## 🏃‍♂️ Running the Application

You will need to open **two** terminal windows to run the app locally. Ensure your virtual environment is activated in both.

**Terminal 1: Start the Celery Worker**
```bash
celery -A config worker --loglevel=info --pool=solo
```
*(Note: `--pool=solo` is used here for compatibility with Windows. If on Mac/Linux, you can omit it).*

**Terminal 2: Start the Django Web Server**
```bash
python manage.py runserver
```

## 💡 How to Use

1. Navigate to the Django Admin at `http://127.0.0.1:8000/admin/` and log in.
2. Create a new **Product** (e.g., "Premium T-Shirt").
3. Create a **Product View** linked to that product. Upload a high-quality base image (e.g., a blank T-shirt) and define the Print Area coordinates (`X`, `Y`, `Width`, `Height`).
4. Navigate to the main application at `http://127.0.0.1:8000/`.
5. Select the product view, upload a `.png` or `.jpg` design, and click **Generate Preview**.
6. Watch as the status updates dynamically and your custom product is rendered!
