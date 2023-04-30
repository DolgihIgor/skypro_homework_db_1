import sqlite3

connection = sqlite3.connect("netflix.db")
cursor = connection.cursor()
sqlite_query = """
    SELECT *
    FROM netflix
"""
cursor.execute(sqlite_query)

for row in cursor.fetchall():
    print(row)

connection.close()
