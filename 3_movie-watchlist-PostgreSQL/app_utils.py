from datetime import datetime 
import database


def prompt_add_movie():

    title = input('Enter movie title: ')

    date = input('Enter release date (dd-mm-YYYY): ')

    parsed_date = datetime.strptime(date, '%d-%m-%Y').timestamp()

    database.add_movies(title, parsed_date)

    return print('Movie added!')


def prompt_watch_movie():

    username = input('Enter your username:')

    title = input('Enter movie title: ')

    database.watch_movie(username, title)


def prompt_add_user():

    username = input('Enter new username: ')

    database.add_user(username)


def prompt_watched_movies():

    username = input('Enter username: ')

    movies = database.get_watched_movies(username)

    if movies:

        print_watched_movie(username, movies)

    else:

        print('This user has not seen any movies yet!')

def prompt_search_movies():

    title = input('Enter movie title: ')

    movies = database.search_movies(title)

    if movies: 

        print_movie_list('Printing found movies', movies)

    else: 

        print('No found movies.')
        

def print_watched_movie(username, movies):

    print(f'\n{username} has watched the following movies\n')

    for movie in movies:

        print(f"Title: {movie[1]}\n")


def print_movie_list(print_msg, movies):

    print(f'{print_msg}\n')

    for movie in movies:

        date_format = datetime.fromtimestamp(movie[2]).strftime('%d-%m-%Y')

        print(f"\nTitle: {movie[1]}\nDate: {date_format}\n")