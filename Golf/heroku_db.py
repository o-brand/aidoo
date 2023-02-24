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
                "NAME": "d5igcq490qf7bb",
                "USER": "vmckibhwnrgrcy",
                "PASSWORD": "226fad9766738bf6206a43c57c34f7257215b4b382afc9538f07ee48e1071cb4",
                "HOST": "ec2-63-32-248-14.eu-west-1.compute.amazonaws.com",
                "PORT": "5432",
                "OPTIONS": {"sslmode": "require"},
            }
