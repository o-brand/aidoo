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

```
python3 manage.py migrate
python3 manage.py flush
python3 manage.py loaddata ../db.json
python3 manage.py runserver
```

more one line fun
```
python3 manage.py migrate && python3 manage.py flush && python3 manage.py loaddata ../db.json
```

Then you are ready and can continue coding as usual. If you want to revert your database to the online database, you can still do that with these commands:

```
python manage.py flush
python manage.py loaddata ../db.json
```

```
python3 manage.py flush
python3 manage.py loaddata ../db.json
```

```
python3 manage.py flush && python3 manage.py loaddata ../db.json
```

***The date of the actual save is 02/04/2023.***


## If you ...

### made changes that should be kept in the database

Then you have to update the db.json by this command:

```
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > ../db.json
```

```
python3 manage.py dumpdata --exclude auth.permission --exclude contenttypes > ../db.json
```

*You have to change the encoding of the JSON file to UTF-8 if an error occurred.*

But before you do that, please be sure that you do not have any irrelevant changes in your database.

If you are ready, then commit the modified file, and run these commands to update the database on Heroku as well:

```
python manage.py flush --settings Aidoo.production
python manage.py loaddata ../db.json --settings Aidoo.production
```

```
python3 manage.py flush --settings Aidoo.production
python3 manage.py loaddata ../db.json --settings Aidoo.production
```

Plus, please update the date of the save in this file.

### made changes to models

Then you must migrate and save the database. You have to run these commands:

```
python manage.py makemigrations
python manage.py migrate
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > ../db.json
python manage.py migrate --settings Aidoo.production
python manage.py flush --settings Aidoo.production
python manage.py loaddata ../db.json --settings Aidoo.production
```

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py dumpdata --exclude auth.permission --exclude contenttypes > ../db.json
python3 manage.py migrate --settings Aidoo.production
python3 manage.py flush --settings Aidoo.production
python3 manage.py loaddata ../db.json --settings Aidoo.production
```

one line fun
```
python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py dumpdata --exclude auth.permission --exclude contenttypes > ../db.json && python3 manage.py migrate --settings Aidoo.production && python3 manage.py flush --settings Aidoo.production && python3 manage.py loaddata ../db.json --settings Aidoo.production
```

*You have to change the encoding of the JSON file to UTF-8 if an error occurred.*

And commit the modified file. Plus, please update the date of the save in this file.
