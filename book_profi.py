import sqlite3

class Book:
    def __init__(self, title, author, description, genres):
        """
        Инициализирует объект книги.

        :param title: Название книги.
        :param author: Автор книги.
        :param description: Описание книги.
        :param genres: Список жанров книги.
        """
        self.title = title
        self.author = author
        self.description = description
        self.genres = genres

class Library:
    def __init__(self, db_file):
        """
        Инициализирует объект библиотеки и подключается к базе данных.

        :param db_file: Путь к файлу базы данных SQLite.
        """
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        Создает таблицу 'books' в базе данных, если она не существует.
        """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                            id INTEGER PRIMARY KEY,
                            title TEXT,
                            author TEXT,
                            description TEXT,
                            genre TEXT
                            )''')
        self.conn.commit()

    def add_book(self, book):
        """
        Добавляет новую книгу в базу данных.

        :param book: Объект класса Book, представляющий добавляемую книгу.
        """
        self.cursor.execute("INSERT INTO books (title, author, description, genre) VALUES (?, ?, ?, ?)",
                            (book.title, book.author, book.description, ",".join(book.genres)))
        self.conn.commit()

    def remove_book(self, book_id):
        """
        Удаляет книгу из базы данных по ее идентификатору.

        :param book_id: Идентификатор книги для удаления.
        """
        self.cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        self.conn.commit()

    def search_books(self, keyword):
        """
        Выполняет поиск книг по ключевому слову или фразе в названии или авторе.

        :param keyword: Ключевое слово или фраза для поиска.
        :return: Список книг, содержащих ключевое слово в названии или авторе.
        """
        self.cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", ('%' + keyword + '%', '%' + keyword + '%'))
        books = self.cursor.fetchall()
        return books

    def filter_books_by_genre(self, genre):
        """
        Выводит список книг определенного жанра.

        :param genre: Жанр книги для фильтрации.
        :return: Список книг, относящихся к указанному жанру.
        """
        self.cursor.execute("SELECT * FROM books WHERE genre LIKE ?", ('%' + genre + '%',))
        books = self.cursor.fetchall()
        return books

    def get_all_books(self):
        """
        Возвращает все книги из базы данных.

        :return: Список всех книг в базе данных.
        """
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        return books

    def __del__(self):
        """
        Закрывает соединение с базой данных при уничтожении объекта.
        """
        self.conn.close()

def display_books(books):
    """
    Отображает список книг.

    :param books: Список книг для отображения.
    """
    print("Список книг:")
    for book in books:
        print(f"{book[0]}. {book[1]} - {book[2]}")

def main():
    library = Library("library.db")

    while True:
        print("\nМеню:")
        print("1. Просмотр списка книг")
        print("2. Поиск книги")
        print("3. Добавление новой книги")
        print("4. Удаление книги")
        print("5. Вывод книг по жанру")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            books = library.get_all_books()
            display_books(books)
        elif choice == "2":
            keyword = input("Введите ключевое слово для поиска: ")
            found_books = library.search_books(keyword)
            display_books(found_books)
        elif choice == "3":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            description = input("Введите описание книги: ")
            genres = input("Введите жанры книги через запятую: ").split(",")
            new_book = Book(title, author, description, genres)
            library.add_book(new_book)
            print("Книга успешно добавлена в библиотеку.")
        elif choice == "4":
            books = library.get_all_books()
            display_books(books)
            book_id = input("Введите номер книги для удаления: ")
            library.remove_book(book_id)
            print("Книга успешно удалена из библиотеки.")
        elif choice == "5":
            genre = input("Введите жанр книги для фильтрации: ")
            filtered_books = library.filter_books_by_genre(genre)
            display_books(filtered_books)
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
