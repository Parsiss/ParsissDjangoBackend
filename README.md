## Parsiss CRM - Backend


### Development

To start repository follow these steps
+ Clone repository
+ **Run `git config core.hooksPath .githooks` to set up git hooks (to prevent server build conflicts)**
+ Create `.env` file in root directory and fill it with environment variables (see `.env.sample`)
+ Create a virtual environment and install necessary libraries (see `requirements.txt`)
+ Run `python manage.py migrate` to create database tables
+ Run `python manage.py runserver` to start development server


### Build and deploy
+ Just execute `pyinstaller django.exe.spec` to build the project
+ Copy `dist/django.exe` to the server
+ Copy `.env` file and place it right next to the executable
+ Run `django.exe runserver --noreload` to start the server

