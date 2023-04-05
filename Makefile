migrate:
	docker-compose exec app alembic -c alembic.ini upgrade head
