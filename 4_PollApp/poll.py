from typing import List, Tuple
import database 
from option import Option
from connection_pool import get_connection


class Poll:

    def __init__(self, title:str, owner:str, _id:int = None):
        self.title = title
        self.owner = owner
        self.id = _id

    def __repr__(self):
        return f'Poll({self.title!r}, {self.owner!r}, {self.id!r})'

    def save(self):
        with get_connection() as connection:
            poll_id = database.create_poll(connection, self.title, self.owner)
            self.id = poll_id

    def add_option(self, text:str):
        Option(self.id, text).save()

    @property
    def options(self) -> List[Option]:
        with get_connection() as connection:
            options = database.get_poll_options(connection, self.id)
            return [Option(option[1], option[2], option[0]) for option in options]


    @classmethod
    def get(cls, poll_id: int) -> "Poll":
        with get_connection() as connection:
            poll = database.get_poll_by_id(connection, poll_id)
        
            return cls(title = poll[1], owner = poll[2], _id = poll[0])

    
    @classmethod
    def get_all(cls) -> List["Poll"]:
        with get_connection() as connection:
            polls = database.get_polls(connection)
            return [cls(title = poll[1], owner = poll[2], _id = poll[0]) for poll in polls]

    @classmethod
    def latest(cls) -> "Poll":
        with get_connection() as connection:
            poll = database.get_latest_poll(connection)
            return cls(title = poll[1], owner = poll[2], _id = poll[0])

    


    


