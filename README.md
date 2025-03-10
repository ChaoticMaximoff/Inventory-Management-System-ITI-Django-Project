# Inventory Management System

## Installation

```
# Clone repository
  git clone https://github.com/ChaoticMaximoff/Inventory-Management-System-ITI-Django-Project.git

# Create a virtualenv
  python3 -m venv venv

# Activate the virtualenv
  source venv/bin/activate or .venv/scripts/activate

# Install all dependencies
  pip install -r requirements.txt

# create a database using postgres pgAdmin or psql
# create a .env file in the root dir of the app
## .env should contain the following
 - SECRET_KEY
 - DEBUG
 - POSTGRES_NAME
 - POSTGRES_USER
 - POSTGRES_PASSWORD

## example:
SECRET_KEY="^7sS$\#^Al^$!^(<MtPRL{@g&gG7Ba"#B=@NuSw%?Kd;7Fo9G>"
DEBUG=True
POSTGRES_NAME=postgres_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# run migration
  python manage.py migrate

# run the development server
  python manage.py runserver

```

Django server available at http://localhost:8000/


