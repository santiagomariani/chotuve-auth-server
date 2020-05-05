if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py db init

python manage.py db migrate

python manage.py db upgrade

python manage.py runserver -h 0.0.0.0 -p 5000
