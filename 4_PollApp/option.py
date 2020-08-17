
from typing import List
import database
from connection_pool import get_connection


class Option:

    def __init__(self, poll_id:int, option_text:str, _id:int = None):
        self.poll_id = poll_id
        self.option_text = option_text
        self.id = _id

    def __repr__(self):
        return f'Option({self.poll_id!r}, {self.option_text!r}, {self.id!r})'


    def save(self):
        with get_connection() as connection:
            option_id = database.create_option(connection, self.poll_id, self.option_text)
            self.id = option_id

    @classmethod
    def get(cls, option_id: int ) -> 'Option':
        with get_connection() as connection:
            option = database.get_option(connection, option_id)

            return cls(option[1], option[2], option[0])

    def vote(self, username: str):
        with get_connection() as connection:
            database.add_poll_vote(connection, username, self.id)
           
        
    @property
    def get_votes(self) -> List['database.Vote']:
        with get_connection() as connection:
            votes = database.get_votes(connection, self.id)
        
            return votes



    








