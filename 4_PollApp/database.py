import os
from datetime import datetime
from contextlib import contextmanager
from typing import List, Tuple


######################### DATA TYPES ######################

Poll = Tuple[int, str, str]
Option = Tuple[int, int, str]
Vote = Tuple[str, int]

######################### QUERYS #########################

# - Create TABLES

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
# - Insert into tables

INSERT_POLL_TABLE = """

    INSERT INTO poll (title, owner) VALUES (%s,%s) RETURNING id;

"""

INSERT_OPTION_TABLE = """

    INSERT INTO option (option, poll_id ) VALUES (%s,%s) RETURNING id;

"""

INSERT_VOTE = """

    INSERT INTO vote (username, option_id) VALUES (%s, %s);

"""
# - Poll querys

SELECT_ALL_POLLS = """

    SELECT 
        *
    FROM poll

"""

SELECT_POLL_WITH_OPTIONS = """

    SELECT
        
        *

    FROM option

    WHERE  
        poll_id = %s;

"""

SELECT_POLL_BY_ID = """

    SELECT
        *
    FROM poll

    WHERE id = %s
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

# - Option querys

SELECT_OPTION_BY_ID = """

    SELECT
        *
    FROM option

    WHERE id = %s

"""

SELECT_VOTES_FOR_OPTION = """

    SELECT
        *
    FROM vote

    where option_id = %s

"""


SELECT_RANDOM_VOTER = """

    SELECT
        *
    FROM vote

    WHERE option_id = %s

    ORDER BY RANDOM()

    LIMIT 1;

"""

######################## FUNCS #########################

@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor    


def create_tables(connection):
    with get_cursor(connection) as cursor:
            cursor.execute(CREATE_POLL_TABLE)
            cursor.execute(CREATE_OPTION_TABLE)
            cursor.execute(CREATE_VOTE_TABLE)

# -- Polls

def create_poll(connection, title: str, owner: str) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_POLL_TABLE, (title, owner))
        return cursor.fetchone()[0]


def get_poll_by_id(connection, poll_id: int) -> Poll:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POLL_BY_ID, (poll_id,))
        return cursor.fetchone()


def get_poll_options(connection, poll_id: int) ->  List[Option] :
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POLL_WITH_OPTIONS, (poll_id,) )
        return cursor.fetchall()

def get_polls(connection) -> List[Poll]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_POLLS)
        return cursor.fetchall()


def get_latest_poll(connection) -> Poll:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_LATEST_POLL)
        return cursor.fetchall()


# -- Options


def create_option(connection, poll_id: int, option_text: str) -> int:
    with get_cursor(connection) as cursor:
        option_id = cursor.execute(INSERT_OPTION_TABLE, (poll_id, option_text))
        return option_id.fetchone()[0]

def get_option(connection, option_id:int) -> Option:
    with get_cursor(connection) as cursor:
            cursor.execute(SELECT_OPTION_BY_ID, (option_id,))
            return cursor.fetchone()


def add_poll_vote(connection, username: str, option_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_VOTE, (username, option_id))


def get_votes(connection, option_id:int) -> List[Vote]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_VOTES_FOR_OPTION, (option_id,))
        return cursor.fetchall()

# - Other querys

def get_poll_and_vote_results(connection, poll_id):
    with get_cursor(connection) as cursor:
        cursor.execute(SHOW_POLL_RESULT, (poll_id,))
        return cursor.fetchall()


def get_random_poll_vote(connection, option_id):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_RANDOM_VOTER, (option_id,))
        return cursor.fetchone()





