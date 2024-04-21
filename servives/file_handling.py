import os
import sys

BOOK_PATH = 'book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    def get_page(page: str):
        index = len(page) - 1
        while index != 0:
            if page[index] in signs:
                return page[:index + 1], index + 1
            index -= 1
        return page, len(page)
    signs = ',.!:;?'
    page = text[start:start + size]

    try:
       if page[-1] not in signs:
           return get_page(page)
       elif page[-1] in signs and text[start + size] not in signs:
           return page, size
       elif page[-1] in signs and page[-2] in signs:
           return get_page(page[:-2])
       elif page[-1] in signs and text[start + size + 1] in signs:

           return get_page(page[:-1])
    except IndexError:

        return text[start:], len(text) - start


# Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    with open(path, mode='r', encoding='utf-8') as file:
        book_text = file.read()
        letters_amout = len(book_text)
        start = 0
        i = 1
        while start <= letters_amout:
            page, c = _get_part_text(book_text, start, PAGE_SIZE)
            book[i] = page.lstrip()
            i += 1
            start += c + 1

# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))

