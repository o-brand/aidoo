def database(test, online):
    if test or not online:
        from Golf.settings import BASE_DIR
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    else:
        import os

        if os.environ.get("DATABASE_URL") is not None:
            import re
            data = re.split("://|:|@|/", os.environ["DATABASE_URL"])

            return {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": data[5],
                "USER": data[1],
                "PASSWORD": data[2],
                "HOST": data[3],
                "PORT": data[4],
                "OPTIONS": {"sslmode": "require"},
            }
        else:
            return {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "d89nu78d2tgrs4",
                "USER": "cbggvrqqdxzvdy",
                "PASSWORD": "abdc2f9264e7d3c32b0e02c60469210cacceab4bcb7f018a12c7edaf493f411b",
                "HOST": "ec2-54-78-233-132.eu-west-1.compute.amazonaws.com",
                "PORT": "5432",
                "OPTIONS": {"sslmode": "require"},
            }
