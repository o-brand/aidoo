# Database

We use PostgreSQL with Heroku, so every change you make locally to the database also appears on the real website. Therefore, we have the db.json file to revert the database.

So, before finishing your work, please reset the database with these commands:

```
python manage.py flush
python manage.py loaddata ../db.json
```

The date of the actual save is 02/02/2023.
