DOCK_COMP = ./srcs/docker-compose.yml

all: build
	docker-compose -f $(DOCK_COMP) up -d

build:
	mkdir -p ./srcs/data/db
	# chmod 777 ./srcs/data/db
	docker-compose -f $(DOCK_COMP) up --build

clean:
	-docker-compose -f $(DOCK_COMP) down -v

fclean: clean
	-docker rmi postgres
	-docker rmi srcs-django
	-docker rmi srcs_django

reset: fclean
	sudo rm -rf ./srcs/data
	sudo find . -type d -name '__pycache__' -exec rm -r {} +
	sudo rm -rf ./srcs/django/ft_transcendence/threejs

re: fclean all

git:
		git add .
		git commit -m "$m"
		git push
		@echo "ALL is on your GIT ✔️"

.PHONY: all build clean fclean re reset git