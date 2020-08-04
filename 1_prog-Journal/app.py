from database import create_database, add_entry, get_entries

create_database()

menu = """Please select one of the following options:
1) Add new entry for today.
2) View entries.
3) Exit.

Your selection: """

welcome = "Welcome to the programming diary!"


def prompt_new_entry():

    content = input("What did you learned today?: ")

    date = input("Enter the date:")

    add_entry(content, date)


def view_entries(entries):

    for entry in entries:

        print(f"{entry['date']}\n{entry['content']}\n\n")
    

while (user_input:= input(menu)) != '3':

    if user_input == '1':

        prompt_new_entry()

    elif user_input == '2':

        view_entries(get_entries())

    else:

        print('Invalid entry, please try again')
