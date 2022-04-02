from utils import get_db_connection


def add_user(username, display_name, pin):
    """
    Add a new user to the database
    Required tables: users
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO users
                (username, display_name, pin)
                    VALUES
                    (%s, %s, %s);""", (username, display_name, pin))
            connection.commit() #commit or rollback either is fine


def username_available(username):
    """
    Return True if a username is taken, or False otherwise
    Required tables: users u
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT *
                        FROM users u
                        WHERE u.username = %s;""", (username,)) # using tuple - if we're just using one, we need to add , in the end
            results = cursor.fetchall() # grab all result from the query
            if len(results) > 0:
                return False
            else:
                return True

def get_user_with_credentials(username, pin):
    """
    Return a user id (if it exists) given a username and pin
    Required columns: u.id
    Required tables: users u
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            # Example - this one is filled in for you
            cursor.execute("""SELECT u.id
                              FROM users u
                              WHERE u.username = %s
                              AND u.pin = %s""", (username, pin))
            user_ids = cursor.fetchall()
            if len(user_ids) > 0:
                return user_ids[0][0]  # Return the id from the first (and hopefully only) row


def search_users(name):
    """
    Get all users whose username or display name is like a particular name
    Required columns: u.id, u.username, u.display_name
    Required tables: users u
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT u.id, u.username, u.display_name
                            FROM users u
                            WHERE u.username LIKE CONCAT('%', %s, '%')
                            OR u.display_name LIKE CONCAT('%', %s, '%');""", (name, name))
            results = cursor.fetchall()
            return results

def get_user_details(user_id):
    """
    Return details of a specific user
    Required columns: u.id, u.username, u.display_name
    Required tables: users u
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
           cursor.execute("""SELECT u.id, u.username, u.display_name
                            FROM users u
                            WHERE u.id = %s;""", (user_id,))
           results = cursor.fetchall()
           if len(results) > 0:
               return results[0]
