# nanosemantika_test

## О проекте
Это тестовое задание для компании «Наносемантика»  
Т.З. - Реализовать CRUD для хранения Рецептов используя FastAPI

## Локальный запуск

Первым делом стоит подготовить `.env` файл.  
Пример переменных окружения лежит в `.env.example`

Собираем приложение с помощью:

```
docker-compose build
```
Запускаем приложение:
```
docker-compose up
```
Применяем миграции:
```
make migrate
```
Табличка ingredients заполняется небольшим колличеством ингредиентов  
из которых можно постить рецепты