import os
import psycopg2
from typing import List, Tuple
import random
import database
from connection_pool import get_connection
from poll import Poll
from option import Option


MENU_PROMPT = """-- Menu --

    1) Create new poll
    2) List open polls
    3) Vote on a poll
    4) Show poll votes
    5) Select a random winner from a poll option
    6) Exit

    Enter your choice: """

NEW_OPTION_PROMPT = "Enter new option text (or leave empty to stop adding options): "


def prompt_create_poll():
    poll_title = input("Enter poll title: ")
    poll_owner = input("Enter poll owner: ")
    poll = Poll(title = poll_title, owner = poll_owner)
    poll.save()

    while (new_option := input(NEW_OPTION_PROMPT)):
        poll.add_option(new_option)


def list_open_polls():
    for poll in Poll.get_all():
        print(f"{poll.id}: {poll.title} (created by {poll.owner})")


def prompt_vote_poll():
    poll_id = int(input("Enter poll would you like to vote on: "))

    _print_poll_options(Poll.get(poll_id).options)

    option_id = int(input("Enter option you'd like to vote for: "))
    username = input("Enter the username you'd like to vote as: ")
    
    Option.get(option_id).vote(username)


def _print_poll_options(options: List[Option]):
    for option in options:
        print(f"{option.id}: {option.option_text}")


def show_poll_votes():
    poll_id = int(input("Enter poll you would like to see votes for: "))
    options = Poll.get(poll_id).options
    votes = [len(option.get_votes) for option in options]
    total_votes = sum(votes)

    try:
        for option, vote in zip(options, votes):
            percentage = vote / total_votes * 100.0
            print(f"{option.option_text} got {vote} votes ({percentage:.2f}% of total)")

    except ZeroDivisionError:
        print("No votes yet cast for this poll.")
    


def randomize_poll_winner():
    poll_id = int(input("Enter poll you'd like to pick a winner for: "))
    _print_poll_options(Poll.get(poll_id).options)

    option_id = int(input("Enter which is the winning option, we'll pick a random winner from voters: "))
    votes = Option.get(option_id).get_votes

    winner = random.choice(votes)

    print(f"The randomly selected winner is {winner[0]}.")


MENU_OPTIONS = {
    "1": prompt_create_poll,
    "2": list_open_polls,
    "3": prompt_vote_poll,
    "4": show_poll_votes,
    "5": randomize_poll_winner
}


def menu():
    with get_connection() as connection:
        database.create_tables(connection)
   

    while (selection := input(MENU_PROMPT)) != "6":
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print("Invalid input selected. Please try again.")


menu()