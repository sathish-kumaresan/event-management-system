FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install flask flask-restful

EXPOSE 5001

CMD ["python", "app.py"]

