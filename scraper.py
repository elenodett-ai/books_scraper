"""Парсер каталога книг с сайта Books to Scrape."""

import json
import re
import time
from urllib.parse import urljoin

import requests
import schedule
from bs4 import BeautifulSoup

BASE_URL = 'http://books.toscrape.com/catalogue/'
RATING_MAP = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}


def get_book_data(book_url: str, session=None) -> dict:
    """
    Собирает данные об одной книге со страницы сайта Books to Scrape.

    Args:
        book_url (str): полный URL страницы книги.
        session (requests.Session | None): сессия для повторного
            использования соединения. Если None, используется
            обычный requests.get.

    Returns:
        dict: словарь с данными книги: title, price, rating, in_stock,
            category, description, product_info.

    Raises:
        requests.HTTPError: если сервер вернул код ошибки.
    """
    getter = session or requests
    response = getter.get(book_url, timeout=10)
    response.raise_for_status()
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    main = soup.find('div', class_='product_main')
    title = main.find('h1').text.strip()

    price_text = main.find('p', class_='price_color').text.strip()
    price = float(price_text.lstrip('£'))

    rating_word = main.find('p', class_='star-rating')['class'][1]
    rating = RATING_MAP.get(rating_word, 0)

    availability = main.find('p', class_='availability').text.strip()
    match = re.search(r'\d+', availability)
    in_stock = int(match.group()) if match else 0

    desc_header = soup.find('div', id='product_description')
    description = (desc_header.find_next_sibling('p').text.strip()
                   if desc_header else '')

    breadcrumb = soup.find('ul', class_='breadcrumb').find_all('li')
    category = breadcrumb[2].text.strip()

    table = soup.find('table', class_='table-striped')
    product_info = {row.th.text.strip(): row.td.text.strip()
                    for row in table.find_all('tr')}

    return {
        'title': title,
        'price': price,
        'rating': rating,
        'in_stock': in_stock,
        'category': category,
        'description': description,
        'product_info': product_info,
    }


def scrape_books(is_save: bool = False,
                 file_path: str = 'books_data.txt',
                 max_pages: int | None = None) -> list:
    """
    Собирает данные обо всех книгах каталога Books to Scrape.

    Args:
        is_save (bool): если True, результат сохраняется в файл
            (одна книга в формате JSON на строку).
        file_path (str): путь к файлу для сохранения.
        max_pages (int | None): максимальное число страниц;
            None означает все страницы.

    Returns:
        list[dict]: список словарей с данными книг.
    """
    books = []
    page = 1
    with requests.Session() as session:
        while max_pages is None or page <= max_pages:
            page_url = f'{BASE_URL}page-{page}.html'
            response = session.get(page_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            for article in soup.find_all('article', class_='product_pod'):
                book_url = urljoin(page_url, article.h3.a['href'])
                books.append(get_book_data(book_url, session))
            print(f'Страница {page} готова, всего книг: {len(books)}')

            if soup.find('li', class_='next') is None:
                break
            page += 1

    if is_save:
        with open(file_path, 'w', encoding='utf-8') as file:
            for book in books:
                file.write(json.dumps(book, ensure_ascii=False) + '\n')
    return books


def job():
    """Запускает сбор данных и сохраняет результат в файл."""
    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Старт выгрузки')
    books = scrape_books(is_save=True,
                         file_path='artifacts/books_data.txt')
    print(f'Готово, сохранено книг: {len(books)}')


if __name__ == '__main__':
    schedule.every().day.at('19:00', 'Asia/Omsk').do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)
