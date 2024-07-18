

import json
import os
from typing import List, Dict, Union

BOOKS_FILE = 'library.json'


class Book:
    def __init__(self, title: str, author: str, year: int):
        self.id = self.generate_id()
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"

    def generate_id(self) -> int:
        """Генерация уникального идентификатора для книги."""
        if os.path.exists(BOOKS_FILE):
            with open(BOOKS_FILE, 'r') as file:
                books = json.load(file)
                if books:
                    return max(book['id'] for book in books) + 1
        return 1


class Library:
    def __init__(self):
        self.books = self.load_books()

    def load_books(self) -> List[Dict[str, Union[int, str]]]:
        """Загрузка книг из файла."""
        if os.path.exists(BOOKS_FILE):
            with open(BOOKS_FILE, 'r') as file:
                return json.load(file)
        return []

    def save_books(self):
        """Сохранение книг в файл."""
        with open(BOOKS_FILE, 'w') as file:
            json.dump(self.books, file, indent=4, ensure_ascii=False)

    def add_book(self, title: str, author: str, year: int):
        """Добавление книги в библиотеку."""
        new_book = Book(title, author, year)
        self.books.append(vars(new_book))
        self.save_books()
        print(f"Книга '{title}' добавлена в библиотеку с id {new_book.id}.")

    def remove_book(self, book_id: int):
        """Удаление книги из библиотеки."""
        book = next((book for book in self.books if book['id'] == book_id), None)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Книга с id {book_id} удалена из библиотеки.")
        else:
            print(f"Книга с id {book_id} не найдена.")

    def find_books(self, title: str = "", author: str = "", year: Union[int, str] = "") -> List[Dict[str, Union[int, str]]]:
        """Поиск книг по названию, автору или году издания."""
        results = [book for book in self.books if (title.lower() in book['title'].lower()) or
                                                 (author.lower() in book['author'].lower()) or
                                                 (str(year) == str(book['year']))]
        return results

    def display_books(self):
        """Отображение всех книг в библиотеке."""
        if self.books:
            for book in self.books:
                print(f"id: {book['id']}, title: {book['title']}, author: {book['author']}, year: {book['year']}, status: {book['status']}")
        else:
            print("В библиотеке нет книг.")

    def change_status(self, book_id: int, new_status: str):
        """Изменение статуса книги."""
        book = next((book for book in self.books if book['id'] == book_id), None)
        if book:
            if new_status in ["в наличии", "выдана"]:
                book['status'] = new_status
                self.save_books()
                print(f"Статус книги с id {book_id} изменен на '{new_status}'.")
            else:
                print("Некорректный статус. Используйте 'в наличии' или 'выдана'.")
        else:
            print(f"Книга с id {book_id} не найдена.")


def main():
    library = Library()

    while True:
        print("\nМеню управления библиотекой:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите опцию: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания книги: ")
            if year.isdigit():
                library.add_book(title, author, int(year))
            else:
                print("Год издания должен быть числом.")

        elif choice == '2':
            book_id = input("Введите id книги, которую хотите удалить: ")
            if book_id.isdigit():
                library.remove_book(int(book_id))
            else:
                print("id книги должен быть числом.")

        elif choice == '3':
            title = input("Введите название книги для поиска (оставьте пустым для пропуска): ")
            author = input("Введите автора книги для поиска (оставьте пустым для пропуска): ")
            year = input("Введите год издания книги для поиска (оставьте пустым для пропуска): ")
            results = library.find_books(title, author, year)
            if results:
                for book in results:
                    print(f"id: {book['id']}, title: {book['title']}, author: {book['author']}, year: {book['year']}, status: {book['status']}")
            else:
                print("Книги не найдены.")

        elif choice == '4':
            library.display_books()

        elif choice == '5':
            book_id = input("Введите id книги, для которой хотите изменить статус: ")
            new_status = input("Введите новый статус книги ('в наличии' или 'выдана'): ")
            if book_id.isdigit():
                library.change_status(int(book_id), new_status)
            else:
                print("id книги должен быть числом.")

        elif choice == '6':
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Пожалуйста, выберите снова.")


if __name__ == "__main__":
    main()



