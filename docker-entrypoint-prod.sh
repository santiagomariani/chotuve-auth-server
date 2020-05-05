# TODO: add script to wait posgre databse
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

gunicorn -b :$PORT run:app