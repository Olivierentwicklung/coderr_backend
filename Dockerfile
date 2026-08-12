FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV SECRET_KEY=build-only-secret-key
ENV DEBUG=False
ENV ALLOWED_HOSTS=localhost

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN DJANGO_SETTINGS_MODULE=core.test_settings python manage.py collectstatic --noinput

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8080"]
