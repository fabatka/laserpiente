FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -yqq libpq-dev python3-dev gcc
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "la_serpiente.py"]
