#!/usr/bin/env bash

wait-for-it $DB_HOST:$DB_PORT -t 10

uvicorn app.app:app --reload --port $APP_PORT --host $APP_HOST
