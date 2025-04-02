# Auto-generated by the "new-dockerfile" CLI tool
# Please report any issues to: https://github.com/flexstack/new-dockerfile/issues
ARG VERSION=3.12
ARG BUILDER=docker.io/library/python
FROM ${BUILDER}:${VERSION}-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends wget ca-certificates && apt-get clean && rm -f /var/lib/apt/lists/*_*
RUN update-ca-certificates 2>/dev/null || true
RUN addgroup --system nonroot && adduser --system --ingroup nonroot nonroot
RUN chown -R nonroot:nonroot /app
RUN mkdir -p /var/cache
RUN chown -R nonroot:nonroot /var/cache

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR='/var/cache/pypoetry'
ENV POETRY_HOME='/usr/local'

COPY --chown=nonroot:nonroot . .
ARG INSTALL_CMD="pip install poetry && poetry install --no-ansi --no-root"
RUN if [ ! -z "${INSTALL_CMD}" ]; then sh -c "$INSTALL_CMD";  fi
RUN poetry run python manage.py makemigrations
RUN poetry run python manage.py migrate


ENV PORT=8000
EXPOSE ${PORT}
USER nonroot:nonroot

ARG START_CMD="poetry run python manage.py runserver 0.0.0.0:${PORT}"
ENV START_CMD=${START_CMD}	
RUN if [ -z "${START_CMD}" ]; then echo "Unable to detect a container start command" && exit 1; fi
CMD ${START_CMD}