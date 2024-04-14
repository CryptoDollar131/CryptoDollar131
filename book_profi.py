import sqlite3

class Library:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                book_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author_id INTEGER,
                description TEXT,
                genre_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES Authors(author_id),
                FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Authors (
                author_id INTEGER PRIMARY KEY,
                author_name TEXT NOT NULL UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Genres (
                genre_id INTEGER PRIMARY KEY,
                genre_name TEXT NOT NULL UNIQUE
            )
        ''')
        self.conn.commit()

    def add_book(self, title, author_name, description, genre_name):
        author_id = self.get_or_create_author(author_name)
        genre_id = self.get_or_create_genre(genre_name)
        self.cursor.execute('''
            INSERT INTO Books (title, author_id, description, genre_id) VALUES (?, ?, ?, ?)
        ''', (title, author_id, description, genre_id))
        self.conn.commit()

    def get_or_create_author(self, author_name):
        self.cursor.execute('SELECT author_id FROM Authors WHERE author_name = ?', (author_name,))
        author_id = self.cursor.fetchone()
        if author_id:
            return author_id[0]
        else:
            self.cursor.execute('INSERT INTO Authors (author_name) VALUES (?)', (author_name,))
            self.conn.commit()
            return self.cursor.lastrowid

    def get_or_create_genre(self, genre_name):
        self.cursor.execute('SELECT genre_id FROM Genres WHERE genre_name = ?', (genre_name,))
        genre_id = self.cursor.fetchone()
        if genre_id:
            return genre_id[0]
        else:
            self.cursor.execute('INSERT INTO Genres (genre_name) VALUES (?)', (genre_name,))
            self.conn.commit()
            return self.cursor.lastrowid

    def search_books(self, keyword):
        self.cursor.execute('''
            SELECT title, author_name FROM Books
            JOIN Authors ON Books.author_id = Authors.author_id
            WHERE title LIKE ? OR author_name LIKE ?
        ''', ('%' + keyword + '%', '%' + keyword + '%'))
        return self.cursor.fetchall()

    def view_books(self, genre_name=None):
        if genre_name:
            self.cursor.execute('''
                SELECT title, author_name FROM Books
                JOIN Authors ON Books.author_id = Authors.author_id
                JOIN Genres ON Books.genre_id = Genres.genre_id
                WHERE genre_name = ?
            ''', (genre_name,))
        else:
            self.cursor.execute('''
                SELECT title, author_name FROM Books
                JOIN Authors ON Books.author_id = Authors.author_id
            ''')
        return self.cursor.fetchall()

    def delete_book(self, title):
        self.cursor.execute('DELETE FROM Books WHERE title = ?', (title,))
        self.conn.commit()

    def close(self):
        self.conn.close()

def display_books(books):
    if not books:
        print("Нет книг для отображения.")
    else:
        for i, book in enumerate(books, 1):
            print(f"{i}. {book[0]} by {book[1]}")

def main():

    library = Library('library.db')

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
            books = library.view_books()
            display_books(books)
        elif choice == "2":
            keyword = input("Введите ключевое слово для поиска: ")
            found_books = library.search_books(keyword)
            display_books(found_books)
        elif choice == "3":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            description = input("Введите описание книги: ")
            genre = input("Введите жанр книги: ")
            library.add_book(title, author, description, genre)
            print("Книга успешно добавлена в библиотеку.")
        elif choice == "4":
            title = input("Введите название книги для удаления: ")
            library.delete_book(title)
            print("Книга успешно удалена из библиотеки.")
        elif choice == "5":
            genre = input("Введите жанр книги для фильтрации: ")
            filtered_books = library.view_books(genre)
            display_books(filtered_books)
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

    library.close()

if __name__ == "__main__":
    main()
