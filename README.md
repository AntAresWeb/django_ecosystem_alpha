# django_ecosystem_alpha
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

### Магазин продуктов
Проект выполнен по [тестовому заданию](docs/Тестовое_Джанго_Экосистема_Альфа.docx) для демонстрации моих знаний и навыков использования Python, Django (ORM, DRF),проектирования базы данных.
В ходе выполнения задания спроектирована база данных [соответствующая схеме](https://dbdiagram.io/d/Copy-of-product_shop-6667432e6bc9d447b152faf1)


### Запуск проекта

Клонировать репозиторий. Войти в каталог django_ecosystem_alpha и запустить скрипт install.sh, который создаст окружение, базу данных и заполненит её тестовой информацией:
sh install.sh

Запускать проект скриптом:
sh run_project.sh

Примечание:
При заполнении БД тестовыми данными создаются пользователи с именами User_0, User_1, User_2. Пароль у всех для простоты использования: 12345 

### Примеры использования эндпоинтов

 - получить токен (Bearer Token) для зарегистрированного пользователя
POST http://localhost:8000/api/token/

Информация в запросе:
{
    "username": "username",
    "password": "password"
}

 - освежить токен
POST http://localhost:8000/api/token/refresh/ 

Информация в запросе:
{
    "refresh": [
        "Обязательное поле."
    ]
}

Запросы, не требующие авторизации

- получить список продуктов
GET http://localhost:8000/api/products/

- получить список категорий и подкатегорий
GET http://localhost:8000/api/categories/


Запросы, требующие авторизации

- получить список корзин
GET http://localhost:8000/api/shoppingcarts/

- получить корзину с индексом id
GET http://localhost:8000/api/shoppingcarts/id/

- очистить корзину с индексом id, т.е. удаляются все позиции продуктов из корзины, а сама корзина не удаляется
POST http://localhost:8000/api/shoppingcarts/id/clean/

- добавить в корзину с индексом id продукт
POST http://localhost:8000/api/shoppingcarts/id/product/

Информация в запросе:
{
    "product": id_продукта,
    "quantity": количество_продукта
}

- изменить в корзине с индексом id количество продукта
PATCH http://localhost:8000/api/shoppingcarts/id/product/

Информация в запросе:
{
    "product": id_продукта,
    "quantity": новое_количество_продукта
}

- удалить из корзины с индексом id продукт
DELETE http://localhost:8000/api/shoppingcarts/id/product/

Информация в запросе:
{
    "product": id_продукта,
}

