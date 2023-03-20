def database(test, online):
    if test or not online:
        from Aidoo.settings import BASE_DIR
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
                "NAME": "d6upqgtvti60tc",
                "USER": "kennyauhjykjam",
                "PASSWORD": "f5c5a1f625f2b231f1aece080d5fdb164c8a893e9df4d106f9aa575874e466a8",
                "HOST": "ec2-52-211-216-62.eu-west-1.compute.amazonaws.com",
                "PORT": "5432",
                "OPTIONS": {"sslmode": "require"},
            }
