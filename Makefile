settings = --settings=config.django.local

.PHONY: start
start:
	@printf "[exec] Python Django Start!!!\n"; \
	python manage.py runserver $(settings);

.PHONY: makemigrations
makemigrations:
	python manage.py makemigrations $(settings);

.PHONY: migrate
migrate:
	python manage.py migrate $(settings);

.PHONY: up
up:
	docker-compose -f deploy/local/docker-compose.yml up -d

.PHONY: down
down:
	docker-compose -f deploy/local/docker-compose.yml down

.PHONY: exec
exec:
	@docker compose -f deploy/local/docker-compose.yml ps
	@printf "[exec] 서비스 이름: "; \
	read service; \
	docker compose -f deploy/local/docker-compose.yml exec $$service /bin/bash;

.PHONY: volume
volume:
	@docker volume ls
	@printf "[delete] 볼륨 이름: "; \
	read volume; \
	docker volume rm $$volume;
