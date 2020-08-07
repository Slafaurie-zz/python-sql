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
        release_timestamp REAL,
        watched INTEGER 
        );
"""

INSERT_MOVIES_TABLE = """

    INSERT INTO movies (title, release_timestamp, watched) VALUES (?,?, 0);

"""

UPDATE_MOVIE_TABLES = """

    UPDATE TABLE movies 

    SET
        watched = 1 

    WHERE title = ?;

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

        *

    FROM movies

    WHERE watched = 1;

"""

######################### FUNCS #########################

def create_tables():

    with connection:
        connection.execute(CREATE_MOVIES_TABLE)


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


def update_movie(title):

    with connection:

        cursor = connection.cursor()

        cursor.execute(UPDATE_MOVIE_TABLES, (title,))

        return cursor.fetchall()

def get_watched_movies():

    with connection:

        cursor = connection.cursor()

        cursor.execute(VIEW_WATCHED_MOVIES)

        return cursor.fetchall()
