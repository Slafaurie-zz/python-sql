import sqlite3
from datetime import datetime


######################### START CONNECTION TO SQLITE 3 #########################
connection = sqlite3.connect('data.db')

#return queries as dict
connection.row_factory = sqlite3.Row


######################### QUERYS #########################

CREATE_MOVIES_TABLE = """

    CREATE TABLE IF NOT EXISTS movies(
        id INTEGER PRIMARY KEY,
        title TEXT, 
        release_timestamp REAL
        );
"""

CREATE_WATCH_TABLE = """

    CREATE TABLE IF NOT EXISTS watch(
        user_username TEXT, 
        movie_id INTEGER,
        FOREIGN KEY(user_username) REFERENCES users(username),
        FOREIGN KEY(movie_id) REFERENCES movies(id)
        );
"""

CREATE_USER_TABLE = """

    CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY
            );

"""

INSERT_MOVIES_TABLE = """

    INSERT INTO movies (id, title, release_timestamp) VALUES (NULL,?,?);

"""

INSERT_USERS_TABLE = """

    INSERT INTO users (username) VALUES (?);

"""

INSERT_WATCH_TABLE = """

    INSERT INTO watch (user_username, movie_id) VALUES (?, (SELECT id FROM movies WHERE title = ?));

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

        user_username,
        movie_id,
        title
    
    FROM watch w

    LEFT JOIN movies m

        ON w.movie_id = m.id

    WHERE  
        user_username = ?;

"""

SEARCH_MOVIES = """

    SELECT

        *

    FROM movies

    WHERE title like ?;



"""

######################### FUNCS #########################

def create_tables():

    with connection:
        connection.execute(CREATE_MOVIES_TABLE)

        connection.execute(CREATE_WATCH_TABLE)

        connection.execute(CREATE_USER_TABLE)


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


def add_user(username):

    with connection:

        connection.execute(INSERT_USERS_TABLE, (username,))



def get_watched_movies(username):

    with connection:

        cursor = connection.cursor()

        cursor.execute(VIEW_WATCHED_MOVIES, (username,))

        return cursor.fetchall()


def search_movies(title):

    with connection:

        cursor = connection.cursor()

        cursor.execute(SEARCH_MOVIES, (f'%{title}%',))

        return cursor.fetchall()
