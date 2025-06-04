Django + PostgreSQL Project Setup Guide
Prerequisites
Python 3.8+

PostgreSQL 13+

pip (Python package manager)

Virtualenv (recommended)

Project Initialization
1. Create project directory
bash
mkdir my_django_project
cd my_django_project
2. Set up virtual environment
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Django
bash
pip install django
4. Create Django project
bash
django-admin startproject config .
5. Create your first app
bash
python manage.py startapp core
PostgreSQL Setup
1. Install PostgreSQL dependencies
bash
sudo apt-get install libpq-dev postgresql postgresql-contrib  # Ubuntu/Debian
brew install postgresql                                      # Mac
2. Install Python PostgreSQL adapter
bash
pip install psycopg2-binary