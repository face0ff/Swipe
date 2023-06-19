setup:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py init_admin
	gunicorn swipe.wsgi:application --bind 0.0.0.0:8000


