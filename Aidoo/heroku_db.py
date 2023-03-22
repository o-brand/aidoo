def database(test, online):
    if test or not online:
        from Aidoo.settings import BASE_DIR
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    else:
        import os
        import re

        if os.environ.get("DATABASE_URL") is not None:
            data = os.environ["DATABASE_URL"]
        else:
            configuration = open('../production.txt', 'r')
            data = configuration.readlines()[0].strip()

        data = re.split("://|:|@|/", data)

        return {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": data[5],
                "USER": data[1],
                "PASSWORD": data[2],
                "HOST": data[3],
                "PORT": data[4],
                "OPTIONS": {"sslmode": "require"},
            }
