# Database

We use PostgreSQL with Heroku, so every change you make locally to the database also appears on the real website. Therefore, we have the db.json file to revert the database.

So, before finishing your work, please reset the database with these commands:

```
python manage.py flush
python manage.py loaddata ../db.json
```

***The date of the actual save is 04/02/2023.***


## If you ...

### made changes that should be kept in the database

Then you have to update the db.json by this command:

```
python manage.py dumpdata > ../db.json
```

And commit the modified file. Plus, please update the date of the save in this file.

### made changes to models

Then you must migrate and save the database. You have to run these commands:

```
python manage.py makemigrations
python manage.py migrate
python manage.py dumpdata > ../db.json
```

And commit the modified file. Plus, please update the date of the save in this file.
