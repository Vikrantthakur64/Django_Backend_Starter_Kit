# Install dependencies
pip install -r requirements.txt

# Make migrations
python manage.py makemigrations users

# Migrate database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver 