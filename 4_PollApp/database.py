import os
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values


######################### QUERYS #########################

CREATE_POLL_TABLE = """

    CREATE TABLE IF NOT EXISTS poll(
        id SERIAL PRIMARY KEY,
        title TEXT, 
        owner TEXT
        );
"""

CREATE_OPTION_TABLE = """

    CREATE TABLE IF NOT EXISTS option(
        id SERIAL PRIMARY KEY, 
        poll_id INTEGER,
        option TEXT,
        FOREIGN KEY(poll_id) REFERENCES poll(id)
        );
"""

CREATE_VOTE_TABLE = """

    CREATE TABLE IF NOT EXISTS vote(
            username TEXT,
            option_id INTEGER,
            FOREIGN KEY(option_id) REFERENCES option(id)
            );

"""

INSERT_POLL_TABLE = """

    INSERT INTO poll (title, owner) VALUES (%s,%s) RETURNING id;

"""

INSERT_OPTION_TABLE = """

    INSERT INTO option (option, poll_id ) VALUES %s;

"""

INSERT_VOTE = """

    INSERT INTO vote (username, option_id) VALUES (%s, %s);

"""

SELECT_ALL_POLLS = """

    SELECT 
        *
    FROM poll

"""

SELECT_POLL_WITH_OPTIONS = """

    SELECT
        
    *

    FROM poll

    JOIN option 
        on poll.id = option.poll_id

    WHERE  
        poll_id = %s;

"""

SHOW_POLL_RESULT = """

    SELECT


        option.id,
        option.option,
        count(vote.option_id) as votes,
        count(vote.option_id) / sum(count(vote.option_id)) over() * 100.0 AS vote_percentage

    FROM option

    LEFT JOIN vote

        on vote.option_id = option.id

    WHERE option.poll_id = %s
    
    GROUP BY 1,2;

"""

SEARCH_POLL_TITLE = """

    SELECT
        *
    FROM poll

    WHERE title like %s
"""

SELECT_LATEST_POLL = """

    SELECT

        *

    FROM option

    WHERE poll_id = (

        SELECT
            id
        FOM poll
        ORDER BY id DESC
        LIMIT 1
    )

"""

SELECT_RANDOM_VOTER = """

    SELECT
        *
    FROM vote

    WHERE option_id = %s

    ORDER BY RANDOM()

    LIMIT 1;

"""

######################### FUNCS #########################

def create_tables(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_POLL_TABLE)
            cursor.execute(CREATE_OPTION_TABLE)
            cursor.execute(CREATE_VOTE_TABLE)


def get_polls(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_POLLS)
            return cursor.fetchall()


def get_latest_poll(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_LATEST_POLL)

            return cursor.fetchall()


def get_poll_details(connection, poll_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_POLL_WITH_OPTIONS, (poll_id,))
            return cursor.fetchall()


def get_poll_and_vote_results(connection, poll_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SHOW_POLL_RESULT, (poll_id,))
            return cursor.fetchall()


def get_random_poll_vote(connection, option_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_RANDOM_VOTER, (option_id,))

            return cursor.fetchone()


def create_poll(connection, title, owner, options):
    with connection:
        with connection.cursor() as cursor:
            
            cursor.execute(INSERT_POLL_TABLE, (title, owner))

            poll_id = cursor.fetchone()[0]

            options_values = [(option, poll_id) for option in options]

            execute_values(cursor, INSERT_OPTION_TABLE, options_values)



def add_poll_vote(connection, username, option_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VOTE, (username, option_id))