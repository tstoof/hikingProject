In de backend doen we alle code voor het schrijven vd algoritmes etc en de frontend en api is de koppeling aan de gebruikerskant

How to set up the environment
https://docs.djangoproject.com/en/5.1/howto/windows/



Dit heb ik al gedaan:
python --version
pip --version
pip install virtualenv
python -m venv hikeEnv
.\hikeEnv\Scripts\activate
pip install django
django-admin --version
django-admin startproject hikingApp
cd hikingApp

python manage.py migrate
## python manage.py runserver   
## python manage.py startapp hike





add apps in settings.py


hike\views.py is important
urls.py is important