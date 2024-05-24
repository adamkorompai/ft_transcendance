DOCK_COMP = ./srcs/docker-compose.yml

all: build

build:
	mkdir -p ./srcs/certificates
	mkdir -p ./srcs/data/db
	mkdir -p ./srcs/data/grafana
	mkdir -p ./srcs/data/prometheus
	docker pull grafana/grafana-oss
	docker-compose -f $(DOCK_COMP) up --build

clean:
	-docker-compose -f $(DOCK_COMP) down -v

fclean: clean
	-docker rmi postgres
	-docker rmi srcs-django
	-docker rmi srcs_django

reset: fclean
	rm -rf ./srcs/data
	rm -rf ./srcs/certificates
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf ./srcs/django/ft_transcendence/threejs

re: fclean all

git:
		git add .
		git commit -m "$m"
		git push
		@echo "ALL is on your GIT ✔️"

.PHONY: all build clean fclean re reset git