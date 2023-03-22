@ECHO OFF

:START
cls

echo "Installling Python"
>nul 2>nul assoc .py

if errorlevel 1 (
	echo "Please Install Python3.6"
	python
	goto END
) else (
	echo "Python is intalled"
)

echo "Installing the Requirements"
cd ..\Aidoo\
python manage.py install requirements.txt

echo "Installation Complete"

echo "Running the Website Locally"

python manage.py runserver

:END

