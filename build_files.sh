echo "Installing dependencies"
python3.9 -m pip install -r requirements.txt

echo "Applying migrations"
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

echo "Build complete"