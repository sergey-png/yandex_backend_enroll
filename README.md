# Yandex Backend Academy Enroll

## Description:
Это вступительное задание в академию бекенда Яндекса.
В этом репозитории реализованы все основные и дополнительные задачи.
REST API написан с использованием FAST API, postgresql, pydantic и менеджера пакетов - poetry.
Использовался Docker контейнер для запуска приложения.
Всего создается три контейнера: для запуска приложения, для запуска базы данных и для запуска PGAdmin 4.


## Commands
Для запуска контейнеров используется команда:
``` make docker ```

### Docker clean, build, up, clean
    make docker

### Up docker container:
    make docker-up

### Down docker container:
    make docker-down

### Create venv (if no docker):
    make venv

### Run app:
    make run

Для запуска тестов этого приложения используется команда:
``` make test ```
### Run tests:
    make test

### Run linters:
    make lint

### Run formatters:
    make format

### Run format and lint code then run tests:
    make check
