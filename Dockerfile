FROM python:3.8

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py refreshrepos

EXPOSE 8000

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]