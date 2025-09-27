FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["gunicorn", "hotel_booking.wsgi:application", "--bind", "0.0.0.0:8000"]