# Описание сервиса
Данный сервис разработан для любителей музыки, которые готовы всем доказать, что их любимая музыка самая лучшая, что другим медведь на ушах польку танцевал...

# Установка
Клонируйте репозиторий на ваш ПК
```
git clone https://github.com/apashovkin48/api_yamdb.git
```
Перейдите в папку с проектом:
```
cd api_yamdb
```
Установите виртуальное окружение и активируйте его:
```
python3 -m venv venv
```
```
source venv/bit/activate
```
Установить зависимости из файла requirements.txt:
```
pip3 install -r requirements.txt
```
Выполнить миграции:
```
cd api_yamdb
```
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```

# Используемые технологии
```
1. Django
2. Django REST Framework
```

# Документация
Подробную информацию по работе с API можно получить из документации:
```
.../redoc/
```

# Кастомные manage команды
Для загрузки в бд тестовых данных используйте команду:
```
python3 manage.py import_db_from_csv
```