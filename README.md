### start een localhost server om te kijken hoe je veranderingen eruit zien

      - cd hikingApp
      - python manage.py runserver

### als de opmaak verdwenen is, ga naar hikingApp/settings.py en zet DEBUG = True

### Voordat je begint, check of je op de goede branch zit (dus niet main)

      - git status
      - git checkout branch_name

### Om een verandering naar git te uploaden, doe dit:

      - git add .
      - git commit -m "hier komt je commit message"
      - git push

### General Workflow Steps:

1.Create a Feature Branch: When starting a new feature, create a branch off of development:

      - git checkout development
      - git checkout -b feature/my-new-feature

2.Work on Your Feature: Make changes and commit them to your feature branch.

3.Push Your Feature Branch: Push your feature branch to GitHub:

      - git push origin feature/my-new-feature

4.Create a Pull Request: When you're ready to merge the feature, open a pull request to merge feature/my-new-feature into development.

5.Review and Merge the Pull Request: After the pull request is reviewed, and tests pass, merge it into the development branch.

6.Merge Development into Main: Once you're satisfied with the development branch and ready to release, create a pull request to merge development into main. This will trigger a final CI check to ensure everything works before merging into main.
