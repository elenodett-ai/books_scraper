# Books Scraper

## Цель проекта
Автоматический сбор данных о книгах с учебного сайта
[Books to Scrape](http://books.toscrape.com): название, цена, рейтинг,
количество в наличии, категория, описание и таблица Product Information.
Сбор запускается автоматически каждый день в 19:00 (Asia/Omsk),
результат сохраняется в текстовый файл.

## Структура проекта

    books_scraper/
    ├── artifacts/
    │   └── books_data.txt              # результат парсинга (JSON Lines)
    ├── notebooks/
    │   └── HW_03_python_ds.ipynb  # ноутбук с решением и выводами
    ├── tests/
    │   └── test_scraper.py             # автотесты pytest
    ├── scraper.py                      # основной скрипт парсера
    ├── pytest.ini                      # настройки pytest
    ├── requirements.txt                # зависимости
    └── .gitignore

## Инструкция по запуску

**1. Клонировать репозиторий:**

    git clone https://github.com/elenodett-ai/books_scraper.git
    cd books_scraper

**2. Создать и активировать виртуальное окружение:**

    python -m venv venv
    venv\Scripts\activate          # Windows
    source venv/bin/activate       # macOS / Linux

**3. Установить зависимости:**

    pip install -r requirements.txt

**4. Запустить парсер по расписанию (каждый день в 19:00):**

    python scraper.py

**5. Запустить тесты:**

    pytest -v

## Используемые библиотеки
- `requests` — HTTP-запросы к страницам сайта
- `beautifulsoup4` — парсинг HTML
- `schedule` — запуск задачи по расписанию
- `pytz` — часовой пояс для расписания
- `pytest` — автотесты
