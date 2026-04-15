from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from books import Book


def print_menu() -> None:
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    return input("Choose an option (1-5): ").strip()


def get_book_details() -> tuple[str, str, int]:
    title = input("Enter book title: ").strip()
    if not title:
        raise ValueError("Title cannot be empty.")

    author = input("Enter author: ").strip()
    if not author:
        raise ValueError("Author cannot be empty.")

    year_input = input("Enter publication year: ").strip()
    year = 0
    if year_input:
        try:
            year = int(year_input)
            if year <= 0:
                raise ValueError("Year must be a positive number.")
        except ValueError as e:
            raise ValueError(f"Invalid year '{year_input}': {e}") from e

    return title, author, year


def print_books(books: list[Book]) -> None:
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
