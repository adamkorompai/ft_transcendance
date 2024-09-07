FROM python:3.9.18-bookworm

RUN apt-get update -y && apt-get upgrade -y nginx
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
				# access environment variables
				python-dotenv \
				# forms styling + bootstrap
				django-crispy-forms \
				crispy-bootstrap5 \
				# for ImageField in models
				Pillow \
				# render specific block in template
				Jinja2 \
				django-render-block \
				# enable ssl certificate
				werkzeug \
				django-extensions \
				pyOpenSSL \
				django-sslserver \
				# enable prometheus metrics export
				django-prometheus

COPY ./ft_transcendence /home/django/ft_transcendence
COPY nginx.conf /etc/nginx/nginx.conf

WORKDIR /home/django/ft_transcendence

COPY ./launch.sh /home/django/launch.sh 

COPY ./nginx.conf /etc/nginx/

RUN chmod +x /home/django/launch.sh

CMD [ "/bin/bash", "/home/django/launch.sh" ]