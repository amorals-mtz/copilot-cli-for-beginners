import sys
from books import Book, BookCollection


# Global collection instance
collection = BookCollection()


def show_books(books: list[Book]) -> None:
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        stars = ""
        if book.rating is not None:
            stars = " " + "★" * book.rating + "☆" * (5 - book.rating)
        review = f" — {book.review}" if book.review else ""
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year}){stars}{review}")

    print()


def handle_list() -> None:
    books = collection.list_books()
    show_books(books)


def handle_add() -> None:
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_remove() -> None:
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)

    print("\nBook removed if it existed.\n")


def handle_find() -> None:
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    show_books(books)


def handle_search() -> None:
    print("\nSearch Books\n")

    query = input("Search by title or author: ").strip()
    if not query:
        print("\nError: search query cannot be empty.\n")
        return

    books = collection.search(query)
    show_books(books)


def handle_rate() -> None:
    print("\nRate a Book\n")

    title = input("Book title: ").strip()
    if not title:
        print("\nError: title cannot be empty.\n")
        return

    rating_str = input("Rating (1-5, leave blank to skip): ").strip()
    rating: int | None = None
    if rating_str:
        try:
            rating = int(rating_str)
        except ValueError:
            print(f"\nError: '{rating_str}' is not a valid number.\n")
            return

    review = input("Review (leave blank to skip): ").strip() or None

    try:
        if collection.rate_book(title, rating=rating, review=review):
            print("\nBook updated successfully.\n")
        else:
            print(f"\nNo book found with title '{title}'.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_mark() -> None:
    print("\nMark a Book as Read\n")

    title = input("Book title: ").strip()
    if not title:
        print("\nError: title cannot be empty.\n")
        return

    if collection.mark_as_read(title):
        print(f"\n'{title}' marked as read.\n")
    else:
        print(f"\nNo book found with title '{title}'.\n")


def show_help() -> None:
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  search   - Search books by title or author
  mark     - Mark a book as read
  rate     - Rate a book and add a review
  help     - Show this help message
""")


COMMANDS = {
    "list": handle_list,
    "add": handle_add,
    "remove": handle_remove,
    "find": handle_find,
    "search": handle_search,
    "mark": handle_mark,
    "rate": handle_rate,
    "help": show_help,
}


def main() -> None:
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()
    handler = COMMANDS.get(command)

    if handler:
        handler()
    else:
        print(f"Unknown command: '{command}'\n")
        show_help()


if __name__ == "__main__":
    main()
