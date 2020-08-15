import os
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

load_dotenv()


######################### START CONNECTION TO POSTGRESQL #########################
connection = psycopg2.connect(os.environ['DATABASE_URL'])

cursor = connection.cursor()

######################### QUERYS #########################

CREATE_MOVIES_TABLE = """

    CREATE TABLE IF NOT EXISTS movies(
        id SERIAL PRIMARY KEY,
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

    INSERT INTO movies (title, release_timestamp) VALUES (%s,%s);

"""

INSERT_USERS_TABLE = """

    INSERT INTO users (username) VALUES (%s);

"""

INSERT_WATCH_TABLE = """

    INSERT INTO watch (user_username, movie_id) VALUES (%s, (SELECT id FROM movies WHERE title = %s));

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

    WHERE release_timestamp > %s;

"""

VIEW_WATCHED_MOVIES = """

    SELECT

        user_username,
        title,
        release_timestamp,
        movie_id
        
    
    FROM watch w

    LEFT JOIN movies m

        ON w.movie_id = m.id

    WHERE  
        user_username = %s;

"""

SEARCH_MOVIES = """

    SELECT

        *

    FROM movies

    WHERE title like %s;



"""

######################### FUNCS #########################

def create_tables():

    with connection:
        with connection.cursor() as cursor:

            cursor.execute(CREATE_MOVIES_TABLE)

            cursor.execute(CREATE_USER_TABLE)

            cursor.execute(CREATE_WATCH_TABLE)


def add_movies(title, release_timestamp):

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES_TABLE, (title, release_timestamp))


def get_movies(upcoming = False):


    with connection:

        with connection.cursor() as cursor:

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

        with connection.cursor() as cursor:

            cursor.execute(INSERT_WATCH_TABLE, (watcher_name, title))


def add_user(username):

    with connection:

        with connection.cursor() as cursor:

            cursor.execute(INSERT_USERS_TABLE, (username,))



def get_watched_movies(username):

    with connection:

        with connection.cursor() as cursor:

            cursor.execute(VIEW_WATCHED_MOVIES, (username,))

            return cursor.fetchall()


def search_movies(title):

    with connection:

        with connection.cursor() as cursor:

            cursor.execute(SEARCH_MOVIES, (f'%{title}%',))

            return cursor.fetchall()
