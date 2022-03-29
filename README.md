# Epic Events

This project is a RESTful API designed for a consulting and event management company.
The application allows users to do basic CRUD operations on 6 major endpoints: customers, customer-details, contracts, contract-details, events, event-details.

A secure database is implemented with Django ORM and PostgreSQL.

This project uses the following technologies
- Django: backend
- DjangoRestFramework: API endpoints
- PostgreSQL: database
- Sentry: logging

## Documentation

For more details on how this API works, please refer to its [documentation](https://www.postman.com/aatroxiss/workspace/epic-events/collection/17750814-052df2cc-576c-4dda-bb24-b1c3c2c6199e?action=share&creator=17750814) (Postman), and the CRM entity-relationship diagram.


## How to install this projet?

### Download and create virtual environment

For this project, you will need to have Python 3.10 installed on you machine. Make sure to also install pip and PostgreSQL 14.2. Then open a terminal and navigate to the directory where you want to install this project.
Now you can run the following commands:

1. From repository download files and clone the folder.
        `code`
        $ git clone https://github.com/AatroXissTV/OC_P12_Epic_Events.git Epic_Events
        $ cd Epic_Events

2. Create a Python environnment.
        `code`
        $ python -m venv venv  # Windows
        $ python3 -m venv venv  # MacOs & Linux

3. Activate the virtual environment.
        `code`
        $ source venv/bin/activate  # MacOS or Linux
        $ source env/Scripts/activate  # for Windows

4. Install the dependencies
        `code`
        $ pip install -r requirements.txt

### Setup sentry and database

As we said earlier, you will need to have PostgreSQL (14.2) installed on your machine. Please refers to PostgreSQL documentation to launch a server.
Then create the databe using SQL shell (psql): CREATE DATABASE epic_events_db

To be more quicly install this project a script has been made. To launch the script run the following commande:
        `code`
        python env_setup.py

You will be asked the database name, username, password, host and port.
Please enter the datas you just used.
This project uses sentry to log errors. Please go on this page and retrieve the dsn variable. 

A Django secret key will be automatically generated.

### Migrate the database

You'll have to then migrate the database running this command:
        `code`
        python manage.py makemigrations
        python manage.py migrate

### Create a super user

The create an admin (supersuser) to access the admin website.
You can create a superuser running this command line:
        `code`
        python manage.py create superuser

### Launching the server

Finally you can launch the server running this command:
        `code`
        python manage.py runserver

## How to use this projet?