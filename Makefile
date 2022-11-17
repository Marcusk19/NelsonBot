init:
	pre-commit autoupdate
	pre-commit install

build:
	docker-compose build

rebuild:
	docker-compose build	
	docker-compose up -d --remove-orphans