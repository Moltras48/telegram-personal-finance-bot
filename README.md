За основу был взят проект "https://github.com/alexey-goloburdin/telegram-finance-bot". Бот был переписан на новую версию aiogram 3, добавлены некоторые функции:
1) Ботом может теперь пользоваться любой человек, который знает пароль, т.е. в базе данных теперь вносятся данные по каждому user_id телеграма.
2) Добавлена возможность изменять дневной Лимит
3) Добавлена возможно выгружать все данные о тратах в файл .xlsx (Данные о тратах ограничены кол-вом размера строк Экселя и передаваемым размером файла в телеграме).

В переменных окружения .env надо проставить TELEGRAM_API_TOKEN и TELEGRAM_BOT_PASSWORD.

`TELEGRAM_API_TOKEN` — API токен бота.

`TELEGRAM_BOT_PASSWORD`  — Пароль для авторизации пользователя в телеграм боте.

При клонировании репозитория с github необходимо создать файл `db/finance.db`, так как github не клонирует пустые файлы.

Использование с Docker показано ниже. Предварительно заполните ENV переменные, указанные выше, в Dockerfile,
В команде запуска укажите локальную директорию(если вдруг хотите её поменять) с проектом вместо `telegram-personal-finance-bot`.
SQLite база данных будет лежать в папке проекта `db/finance.db`.

```
docker compose up - команда для запуска и сбора контенера
```

Чтобы войти в работающий контейнер:

```
docker exec -ti tg_personal_finance_bot sh
```

Войти в контейнере в SQL шелл:

```
docker exec -ti tg_personal_finance_bot sh
sqlite3 /db/finance.db
```


