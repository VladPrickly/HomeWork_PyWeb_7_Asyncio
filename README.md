# Задание 

Выгрузить из API SWAPI персонажей Start Wars и загрузить в базу данных.<br>
Документация по API находится здесь: [SWAPI](https://swapi.tech/). <br>

Необходимо выгрузить cледующие поля:<br>
**id** - ID персонажа <br>
**birth_year** <br>
**eye_color** <br>
**gender** <br>
**hair_color** <br>
**homeworld** <br>
**mass** <br>
**name** <br>
**skin_color** <br>
Данные по каждому персонажу необходимо загрузить в любую базу данных. <br>
Выгрузка из апи и загрузка в базу должна происходить асинхронно. <br>

Результатом работы будет: <br>
1) скрипт миграции базы данных <br>
2) скрипт загрузки данных из API в базу <br>

## Предварительные требования
- Python 3.12+
- Git
- PostgreSQL
- Доступ к интернету

## Установка
1. Создайте виртуальное окружение:
python -m venv .venv

2. Активируйте виртуальное окружение:
- Windows:
  ```
  venv\Scripts\activate
  ```
- Linux/macOS:
  ```
  source venv/bin/activate
  ```
3. Установите зависимости:
pip install -r requirements.txt

4. Запуск приложения:
- запустить Docker Desktop
- создание БД: docker-compose up
- запуск приложения: python main.py

БД будет создана при первом запуске.
