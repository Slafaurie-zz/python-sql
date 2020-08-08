import sqlite3
from datetime import datetime


######################### START CONNECTION TO SQLITE 3 #########################
connection = sqlite3.connect('data.db')

#return queries as dict
connection.row_factory = sqlite3.Row


######################### QUERYS #########################

CREATE_MOVIES_TABLE = """

    CREATE TABLE IF NOT EXISTS movies(
        title TEXT, 
        release_timestamp REAL
        );
"""

CREATE_WATCH_TABLE = """

    CREATE TABLE IF NOT EXISTS watch(
        watcher_name TEXT, 
        title REAL
        );
"""


INSERT_MOVIES_TABLE = """

    INSERT INTO movies (title, release_timestamp) VALUES (?,?);

"""

INSERT_WATCH_TABLE = """

    INSERT INTO watch (watcher_name, title) VALUES (?,?);

"""

VIEW_ALL_MOVIES = """

    SELECT 
        *
    FROM movies

"""

VIEW_UPCOMING_MOVIES = """


    SELECT 
        *
    FROM movies
    WHERE release_timestamp > ?;

"""

VIEW_WATCHED_MOVIES = """

    SELECT

        watcher_name,
        title
        

    FROM watch

    WHERE watcher_name = ?;

"""

DELETE_MOVIES = """

    DELETE FROM movies

    WHERE title = ?;


"""

######################### FUNCS #########################

def create_tables():

    with connection:
        connection.execute(CREATE_MOVIES_TABLE)

        connection.execute(CREATE_WATCH_TABLE)


def add_movies(title, release_timestamp):

    with connection:
        connection.execute(INSERT_MOVIES_TABLE, (title, release_timestamp))


def get_movies(upcoming = False):


    with connection:

        cursor = connection.cursor()


        if upcoming:
        
            timestamp_now = datetime.now().timestamp()

            cursor.execute(VIEW_UPCOMING_MOVIES, (timestamp_now,))

            return cursor.fetchall()

        else:

            cursor.execute(VIEW_ALL_MOVIES)

            return cursor.fetchall()


def watch_movie(watcher_name, title):

    with connection:

        cursor = connection.cursor()

        cursor.execute(INSERT_WATCH_TABLE, (watcher_name, title))

        cursor.execute(DELETE_MOVIES, (title,))


def get_watched_movies(username):

    with connection:

        cursor = connection.cursor()

        cursor.execute(VIEW_WATCHED_MOVIES, (username,))

        return cursor.fetchall()
