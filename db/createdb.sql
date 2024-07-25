CREATE TABLE budget(
    id integer primary key,
    codename varchar(255),
    daily_limit integer,
    telegram_user_id integer,
    FOREIGN KEY(telegram_user_id) REFERENCES users(id)
    );

CREATE TABLE category(
    codename varchar(255) primary key,
    name varchar(255),
    is_base_expense boolean,
    aliases text
    );

CREATE TABLE expense(
    id integer primary key,
    amount integer,
    created datetime,
    category_codename integer,
    raw_text text,
    telegram_user_id integer,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
    FOREIGN KEY(telegram_user_id) REFERENCES users(id)
    );

CREATE TABLE users(
    id integer primary key,
    telegram_id integer unique
    );

INSERT INTO category (codename, name, is_base_expense, aliases) VALUES
    ("products", "Продукты", true, "еда, продукты"),
    ("utilities", "Коммунальные услуги", true, "свет, вода, тепло, газ, кап. ремонт, коммунальные услуги"),
    ("coffee", "Кофе/Чай", true, "кофе, coffee, чай, tea"),
    ("dinner", "Обед", true, "столовая, ланч, бизнес-ланч, бизнес ланч"),
    ("cafe", "Кафе", false, "ресторан, рест, мак, макдональдс, мак, kfc, bc, burger king,"),
    ("transport", "Общ. транспорт", true, "автобус, транспорт"),
    ("taxi", "Такси", false, "яндекс такси, yandex taxi, такси, taxi"),
    ("phone", "Телефон", false, "билайн, связь"),
    ("books", "Книги", false, "литература, литра, лит-ра, книги, книга"),
    ("internet", "Интернет", false, "инет, inet, интернет"),
    ("subscriptions", "Подписки", false, "подписка"),
    ("other", "Прочее", true, "");
