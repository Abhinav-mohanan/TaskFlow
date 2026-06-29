set -o errexit

# Install dependencies
pip install -r requirements.txt

# Gather static files into STATIC_ROOT
python manage.py collectstatic --noinput

# Apply any database migrations
python manage.py migrate