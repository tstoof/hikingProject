In de backend doen we alle code voor het schrijven vd algoritmes etc en de frontend en api is de koppeling aan de gebruikerskant

How to set up the environment
https://docs.djangoproject.com/en/5.1/howto/windows/



belangrijk (ik wil dit automatiseren zodat we dit niet altijd opnieuw hoeven te doen):
- pip install virtualenv (optioneel)
- python -m venv hikeEnv
- .\hikeEnv\Scripts\activate
- pip install django
- django-admin --version (optioneel)
- cd hikingApp
- python manage.py migrate
- python manage.py runserver   


Om een nieuwe app te maken
- python manage.py startapp appName

Krijn, mocht je weer problemen hebben met .\hikeEnv\Scripts\activate, doe dan dit:
- powershell -ExecutionPolicy Bypass -File C:\hiking_project\hikingProject\hikeEnv\Scripts\Activate.ps1


Om een verandering naar git te uploaden, doe dit:
- git add .
- git commit -m "hier komt je commit message"
- git push



add apps in settings.py
hike\views.py is important
urls.py is important


SUPERMARKT