# planomat
Vote Decsision Making Tool in Python


# Install local
python -m pip install poetry
poetry config virtualenvs.in-project true #optional#
poetry install
poetry run python manage.py tailwind install
poetry run python manage.py makemigrations
poetry run python manage.py migrate

# Start local
poetry run python manage.py runserver
