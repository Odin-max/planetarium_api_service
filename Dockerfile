FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock /app/
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

# Copy project files
COPY . /app/

# Collect static (optional, if you have static files)
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start app
CMD ["gunicorn", "src.wsgi:application", "--bind", "0.0.0.0:8000"]
