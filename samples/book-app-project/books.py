import json
from dataclasses import dataclass, asdict
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self):
        self.books: list[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self) -> None:
        """Save the current book collection to JSON atomically."""
        tmp = Path(str(DATA_FILE) + ".tmp")
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump([asdict(b) for b in self.books], f, indent=2)
            tmp.replace(DATA_FILE)
        except OSError as e:
            print(f"Error: could not save collection: {e}")
            tmp.unlink(missing_ok=True)

    def add_book(self, title: str, author: str, year: int) -> Book:
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> list[Book]:
        return self.books

    def find_book_by_title(self, title: str) -> Book | None:
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> list[Book]:
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]

    def search(self, query: str) -> list[Book]:
        """Search books by partial, case-insensitive match on title or author."""
        q = query.lower()
        return [b for b in self.books if q in b.title.lower() or q in b.author.lower()]
