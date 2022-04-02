from utils import get_db_connection


def get_book_rating_for_user(book_id, user_id):
    """
    Get a specific user's rating for a book
    Required columns: r.score, r.review
    Required tables: book_ratings r
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT *
                              FROM book_ratings r
                              WHERE r.book_id = %s
                              AND r.user_id = %s;""", (book_id, user_id))
            results = cursor.fetchall()
            return results


def get_recent_book_ratings(book_id):
    """
    Get 10 most recent ratings for a book
    Required columns: u.id, u.username, u.display_name, r.score, r.review
    Required tables: users u, book_ratings r
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT u.id, u.username, u.display_name, r.score, r.review
                              FROM book_ratings r
                              JOIN users u
                              ON r.user_id = u.id
                              WHERE r.book_id = %s;""", (book_id,))
            results = cursor.fetchall()
            return results

def get_recent_user_ratings(user_id):
    """
    Get 10 most recent ratings for a user
    Required columns: b.id, b.title, b.author, r.score, r.review
    Required tables: books b, book_ratings r
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT b.id, b.title, b.author, r.score, r.review
                              FROM book_ratings r
                              JOIN books b
                              ON r.book_id = b.id
                              WHERE r.user_id = %s;""", (user_id,))
            results = cursor.fetchall()
            return results

def get_recent_follower_ratings(user_id):
    """
    Get 10 most recent ratings from followed users
    Required columns: u.id, u.username, u.display_name, b.id, b.title, b.author, r.score, r.review
    Required tables: users u, followers f, books b, book_ratings r
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT u.id, u.username, u.display_name, b.id, b.title, b.author, r.score, r.review
                              FROM book_ratings r
                              JOIN books b
                              ON r.book_id = b.id
                              JOIN users u
                              ON r.user_id = u.id
                              JOIN followers f
                              ON u.id = f.followed_user_id
                              WHERE f.following_user_id = %s;""", (user_id,))
            results = cursor.fetchall()
            return results

def add_rating(user_id, book_id, score, review):
    """
    Add a user rating for a specific book into the database
    Required tables: book_ratings r
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO book_ratings
                              (user_id, book_id, score, review)
                              VALUES
                              (%s, %s, %s, %s);""", (user_id, book_id, score, review))
            connection.commit()


def remove_rating(user_id, book_id):
    """
    Remove a user rating for a specific book
    Required tables: book_ratings r
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""DELETE FROM book_ratings
                              WHERE user_id = %s
                              AND book_id = %s;""", (user_id, book_id))
            connection.commit()
