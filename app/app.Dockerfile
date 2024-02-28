FROM python:3.8

RUN apt update -y
RUN apt upgrade -y
RUN apt install -y postgresql-client
RUN apt install -y gdal-bin

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH=/restaurant_app

EXPOSE 8000

RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]
