import sqlite3

connection = sqlite3.connect('data.db')

#return queries as dict
connection.row_factory = sqlite3.Row


def create_database():

    with connection:
        connection.execute('CREATE TABLE IF NOT EXISTS entries(content TEXT, date TEXT);')



def add_entry(content, date):

    with connection:
        connection.execute("INSERT INTO entries (content, date) VALUES (?,?)", (content, date)
        )


def get_entries():

    cursor = connection.execute("SELECT * FROM entries")

    return cursor