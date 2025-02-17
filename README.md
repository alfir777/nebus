# Тестовое задание

## Запуск

0. Проверить уже заранее поднятую версию по адресу https://nebus.jatu.ru/docs

1. Клонировать репозиторий или форк

```
git clone https://github.com/alfir777/nebus.git
```

2. Выполнить копирование файла .env_template на .env и выставить свои параметры (опционально)

```
cd nebus/
cp .env_template .env
```

3. Развернуть контейнеры с помощью в docker-compose (https://docs.docker.com/compose/install/)

```
docker compose -f docker-compose.yml up -d
```

4. Перейти по адресу http://localhost:8008/docs#/
