# Database

***If you get ANY error during heroku updates, write to Gábor immediatelly.***

***Only modify the Heroku DATABASE and the JSON file from MAIN!***

We use PostgreSQL with Heroku, but we separated the local and online databases. Therefore, if you open the real website, Django will use the database hosted by Heroku, but when you run locally, you will have your own SQLite database. This way, you can do anything locally without changing the database, and because we updated the gitignore file, the local database will be only yours.

### After this change, you have to run the following commands:

```
python manage.py migrate
python manage.py flush
python manage.py loaddata ../db.json
python manage.py runserver
```

Then you are ready and can continue coding as usual. If you want to revert your database to the online database, you can still do that with these commands:

```
python manage.py flush
python manage.py loaddata ../db.json
```

***The date of the actual save is 20/02/2023.***


## If you ...

### made changes that should be kept in the database

Then you have to update the db.json by this command:

```
python manage.py dumpdata > ../db.json
```

*You have to change the encoding of the JSON file to UTF-8 if an error occurred.*

But before you do that, please be sure that you do not have any irrelevant changes in your database.

If you are ready, then commit the modified file, and run these commands to update the database on Heroku as well:

```
python manage.py flush --settings Golf.production
python manage.py loaddata ../db.json --settings Golf.production
```

Plus, please update the date of the save in this file.

### made changes to models

Then you must migrate and save the database. You have to run these commands:

```
python manage.py makemigrations
python manage.py migrate
python manage.py dumpdata > ../db.json
python manage.py migrate --settings Golf.production
python manage.py flush --settings Golf.production
python manage.py loaddata ../db.json --settings Golf.production
```

*You have to change the encoding of the JSON file to UTF-8 if an error occurred.*

And commit the modified file. Plus, please update the date of the save in this file.
