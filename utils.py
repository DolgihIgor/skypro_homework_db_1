import sqlite3


def get_movie_by_title(title):
    connection = sqlite3.connect("netflix.db")
    cursor = connection.cursor()
    sqlite_query = f"""
        SELECT *
        FROM netflix
        WHERE title = '{title}'
    """
    result = cursor.execute(sqlite_query)
    data = result.fetchone()
    connection.close()
    return {'title': data[2],
            'country': data[5],
            'release_year': data[7],
            'genre': data[1],
            'description': data[5]
            }
