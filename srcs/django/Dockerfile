FROM python:3.9.18-bookworm

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install postgresql-client wget unzip -y
RUN apt-get install curl -y

RUN pip install --upgrade pip
RUN pip install --no-cache-dir psycopg2-binary \
				django \
				djangorestframework \
				django-cors-headers \
				channels \
				channels_postgres \
				daphne \
				whitenoise \
				requests \
				python-dotenv \
				django-crispy-forms \
				crispy-bootstrap5 \
				Pillow \
				Jinja2 \
				django-render-block \
				werkzeug \
				django-extensions \
				pyOpenSSL \
				django-sslserver \
				django-prometheus

COPY ./ft_transcendence /home/django/ft_transcendence

WORKDIR /home/django/ft_transcendence

COPY ./launch.sh /home/django/launch.sh 

RUN chmod +x /home/django/launch.sh

CMD [ "/bin/bash", "/home/django/launch.sh" ]