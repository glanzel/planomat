# planomat
Vote Decsision Making Tool in Python

## Install Local:
requierements:
- python
- npm
- copy data/.env.template to data/.env  
- set DEBUG=True in data/.env (optional: otherwise collectstatic)

python -m pip install poetry  
poetry config virtualenvs.in-project true #optional#  
poetry install
poetry run python manage.py tailwind install  
poetry run python manage.py makemigrations  
poetry run python manage.py migrate  
poetry run python manage.py createsuperuser  

## Insert Test Data (optional)
poetry run python tests/populate_comparison_data.py

## Start local:
poetry run python manage.py tailwind start  
poetry run python manage.py collectstatic (optional if not in DEBUG mode)
// or poetry run python manage.py tailwind build  
poetry run python manage.py runserver  


