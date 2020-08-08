from datetime import datetime
import database

################### messages menu ###################

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies.
4) Add watched movie.
5) View watched movies.
6) Exit

Your selection: """

welcome = "\nWelcome to the watchlist app!\n"

############## funcs ###################

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



def print_watched_movie(username, movies):

    print(f'\n{username} have watched the following movies\n')

    for movie in movies:

        print(f"Title: {movie['title']}\n")


def print_movie_list(print_msg, movies):

    print(f'{print_msg}\n')

    for movie in movies:

        date_format = datetime.fromtimestamp(movie['release_timestamp']).strftime('%d-%m-%Y')

        print(f"\nTitle: {movie['title']}\nDate: {date_format}\n")



################### app ###################


print(welcome)

database.create_tables()

while (user_input:= input(menu)) != '6':

    
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

        username = input('Enter username: ')

        movies = database.get_watched_movies(username)

        print_watched_movie(username, movies)
    
    elif user_input == '6':

        pass
    
    else:

        print('Invalid entry, please try again')