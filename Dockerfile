# Use an official Python runtime as a parent image
FROM python:3.12-alpine
RUN cat /etc/alpine-release

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

# Set the working directory
WORKDIR /app


# Install dependencies
RUN python3 -m pip install poetry
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root

# Copy the project code into the container
COPY . /app/
COPY data/.env.template data/.env

# Install node dependencies	
RUN apk add nodejs-current npm sqlite bash wget

RUN poetry run python manage.py tailwind install
RUN poetry run python manage.py tailwind build
RUN poetry run python manage.py makemigrations
RUN poetry run python3 manage.py collectstatic --noinput

# Ensure entrypoint.sh Vis copied and has the correct permissions
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
CMD ["0.0.0.0","8000"]
