FROM python:3.11.9-slim-bullseye

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /code

EXPOSE 5000

CMD ["python","app.py"]