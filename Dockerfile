FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

ENV PYTHONPATH=/app/src:$PYTHONPATH

CMD ["gunicorn", "hotel_booking.wsgi:application", "--bind", "0.0.0.0:8000"]