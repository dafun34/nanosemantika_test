format:
	poetry run isort .
	poetry run black .

check:
	poetry run isort . --check
	poetry run flake8 .
	poetry run black . --check

migrate:
	docker-compose exec app alembic -c alembic.ini upgrade head
