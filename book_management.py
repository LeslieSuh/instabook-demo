from utils import get_db_connection


def search_books(title):
    """
    Return a list of books whose titles are like a particular title
    Required columns: b.id, b.title, b.author, AVG(r.score)
    Required tables: books b, book_ratings r
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT b.id, b.title, b.author, ROUND(AVG(r.score), 1)
                              FROM books b
                              JOIN book_ratings r
                              ON b.id = r.book_id
                              WHERE b.title LIKE CONCAT('%', %s, '%')
                              GROUP BY b.id;""", (title,))
            results = cursor.fetchall()
            return results

def get_book_details(book_id):
    """
    Return details of a specific book
    Required columns: b.id, b.title, b.author, AVG(r.score)
    Required tables: books b, book_ratings r
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT b.id, b.title, b.author, ROUND(AVG(r.score), 1)
                              FROM books b
                              JOIN book_ratings r
                              ON b.id = r.book_id
                              WHERE b.id = %s
                              GROUP BY b.id;""", (book_id,))
            results = cursor.fetchall()
            if len(results) > 0:
                return results[0]
