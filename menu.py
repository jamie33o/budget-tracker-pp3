from tabulate import tabulate  # table prints
from print_input import input_validator
from questions import questions
from google_sheets import *


def menu(USERNAME):
   
    menu_options = [
        ["\033[30m" , "***Budget Tracker Menu***\nPlease choose an option\033[0m"],
        ["\033[32m1", "Change Username\033[0m"],
        ["\033[32m2", "Change Budget\033[0m"],
        ["\033[32m3", "Add expenses\033[0m"],
        ["\033[32m4", "Update expenses by date\033[0m"],
        ["\033[32m6", "Search expenses by date\033[0m"],
        ["\033[32m7", "Search expenses by keyword and date\033[0m"],
        ["\033[32m7", "Search expenses date\033[0m"],
        ["\033[32m8", "Search savings by date\033[0m"],
    ]

    print(tabulate(menu_options))

    choice = input_validator("number","Please choose an option between 1 and 5")


    if choice == 1:
        while True:
            NEW_USERNAME = input_validator("username",""" Please enter your new username,
                \nIt must be 5 to 10 characters long""")
            username_changed = change_username(USERNAME,NEW_USERNAME)
            if username_changed:
                break

    elif choice == 2:
            NEW_BUDGET = input_validator("number", "Please enter your new budget:")
            change_budget(USERNAME ,NEW_BUDGET) 
    elif choice == 3:
        prices_dict = questions(USERNAME)
        add_expenses(prices_dict)
    elif choice == 4:
        pass
    elif choice == 5:
        pass
    elif choice == 6:
        pass
    elif choice == 7:
        pass
    elif choice == 8:
        pass