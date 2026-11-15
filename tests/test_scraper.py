import pytest

from scraper import get_book_data, scrape_books

BOOK_URL = ('http://books.toscrape.com/catalogue/'
            'a-light-in-the-attic_1000/index.html')
EXPECTED_KEYS = {'title', 'price', 'rating', 'in_stock',
                 'category', 'description', 'product_info'}


@pytest.fixture(scope='module')
def book():
    """Загружает одну книгу один раз для всех тестов модуля."""
    return get_book_data(BOOK_URL)


def test_book_is_dict_with_keys(book):
    assert isinstance(book, dict)
    assert EXPECTED_KEYS.issubset(book.keys())


def test_book_field_values(book):
    assert book['title'] == 'A Light in the Attic'
    assert book['price'] == 51.77
    assert book['category'] == 'Poetry'
    assert book['product_info']['UPC'] == 'a897fe39b1053632'


def test_book_rating_in_range(book):
    assert 1 <= book['rating'] <= 5


def test_scrape_one_page_returns_20_books():
    books = scrape_books(max_pages=1)
    assert len(books) == 20


def test_scrape_saves_file(tmp_path):
    file_path = tmp_path / 'books.txt'
    scrape_books(is_save=True, file_path=file_path, max_pages=1)
    lines = file_path.read_text(encoding='utf-8').splitlines()
    assert len(lines) == 20
