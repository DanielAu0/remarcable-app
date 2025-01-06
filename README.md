# Django Product Search and Filter

This project demonstrates the functionality to model products, categories, and tags using Django. It allows users to search products by description and filter them by category and tags. 

## Libraries Used

- `asgiref==3.8.1`
- `beautifulsoup4==4.12.3`
- `Django==4.2.17`
- `django-bootstrap-v5==1.0.11`
- `django-debug-toolbar==4.4.6`
- `soupsieve==2.6`
- `sqlparse==0.5.3`
- `tzdata==2024.2`
- `urllib3==2.3.0`

## Assumptions

- Each **product** belongs to **one category**.
- A **product** can have **multiple tags**, and products must contain **all the selected tags** for them to appear in the results.
- The **search functionality** is only applied to the **product description**.

## Setup Instructions

1. **Clone the Repository:**

   Clone this repository to your local machine:

   ```bash
   git clone https://github.com/DanielAu0/remarcable-app.git

2. **Navigate to the project:**

   ```bash
   cd remarcable-app
   
3. **Set up virtual environment and activate (Optional)**

   ```bash
   python -m venv venv

   .\venv\Scripts\activate
   
4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   
5. **Run migrations to create database**

   ```bash
   python manage.py migrate
   
6. **Run the Django development server**

   ```bash
   python manage.py runserver

7. **Navigate to http://127.0.0.1:8000**
