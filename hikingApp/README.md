In de backend doen we alle code voor het schrijven vd algoritmes etc en de frontend en api is de koppeling aan de gebruikerskant

How to set up the environment
https://docs.djangoproject.com/en/5.1/howto/windows/

belangrijk voor de eerste keer (ik wil dit automatiseren zodat we dit niet altijd opnieuw hoeven te doen):

- pip install virtualenv (optioneel)
- python -m venv hikeEnv
- .\hikeEnv\Scripts\activate
- pip install django
- django-admin --version (optioneel)
- cd hikingApp
- python manage.py migrate
- python manage.py runserver

als je de app wil starten:

- .\hikeEnv\Scripts\activate
- cd hikingApp
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





# General Workflow Steps:

1. Create a Feature Branch: When starting a new feature, create a branch off of development:
    - git checkout development
    - git checkout -b feature/my-new-feature

2. Work on Your Feature: Make changes and commit them to your feature branch.

3. Push Your Feature Branch: Push your feature branch to GitHub:
    - git push origin feature/my-new-feature
This will trigger the CI pipeline.

4. Create a Pull Request: When you're ready to merge the feature, open a pull request to merge feature/my-new-feature into development.

5. Review and Merge the Pull Request: After the pull request is reviewed, and tests pass, merge it into the development branch.

6. Merge Development into Main: Once you're satisfied with the development branch and ready to release, create a pull request to merge development into main. This will trigger a final CI check to ensure everything works before merging into main.