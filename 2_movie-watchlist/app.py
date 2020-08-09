from datetime import datetime
import database
from app_utils import *

################### messages menu ###################

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies.
4) Add watched movie.
5) View watched movies.
6) Add user.
7) Search movie.
8) Exit.

Your selection: """

welcome = "\nWelcome to the watchlist app!\n"

################### app ###################

print(welcome)

database.create_tables()

while (user_input:= input(menu)) != '8':

    
    if user_input == '1':

        prompt_add_movie()

    elif user_input == '2':

        movies = database.get_movies(upcoming = True)

        print_movie_list('Upcoming movies', movies)

    elif user_input == '3':

        movies = database.get_movies()

        print_movie_list('All movies', movies)

    elif user_input == '4':

        prompt_watch_movie()

    elif user_input == '5':

        prompt_watched_movies()
    
    elif user_input == '6':

        prompt_add_user()

    elif user_input == '7':

       prompt_search_movies()

    elif user_input == '8':

        pass

    else:

        print('Invalid entry, please try again')