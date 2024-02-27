FROM python:3.8

RUN apt update -y
RUN apt upgrade -y
RUN apt install -y postgresql-client
RUN apt install -y gdal-bin


WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# ENV PYTHONPATH=/app
ENV PYTHONPATH=/restaurant_app

EXPOSE 8000

# CMD ["gunicorn", "restaurant_app.wsgi:application", "--bind", "0.0.0.0:8000"]
# CMD ["python", "manage.py", "runserver"]
# CMD ["python", "manage.py", "runserver", "104.214.236.162:8000"]

#RUN sleep 20

#RUN python manage.py makemigrations
#RUN python manage.py migrate
#RUN python manage.py runserver 104.214.236.162:8000
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#RUN python manage.py makemigrations
#RUN python manage.py migrate

#CMD ["gunicorn", "restaurant_app.wsgi:application", "--bind", "0.0.0.0:8000"]
RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]
