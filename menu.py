from tabulate import tabulate  # table prints
from print_input import input_validator
from questions import questions
from google_sheets import *


def menu(USERNAME):
    
    register(USERNAME)

    prices = {# dictionary matching google sheets expenses work sheet
        "username": USERNAME,
        "date": "",
        "work-commute": 0,
        "work-lunch": 0,
        "kids-commute": 0,
        "kids-lunch": 0,
        "adult-school-commute": 0,
        "adult-school-lunch": 0,
        "shopping": 0,
        "eat-out": 0,
        "small-shop-runs": 0,
        "household":0,
    }
   
    menu_options = [
        ["\033[30m" , "***Budget Tracker Menu***\nPlease choose an option\033[0m"],
        ["\033[32m1", "Change Username\033[0m"],
        ["\033[32m2", "Change Budget\033[0m"],
        ["\033[32m3", "Add/update today's expenses\033[0m"],
        ["\033[32m4", "Update expenses by date\033[0m"],
        ["\033[32m5", "Search budget overview by date\033[0m"],
        ["\033[32m6", "View budget overview \033[0m"],
        ["\033[32m8", "Search savings by date\033[0m"],
        ["\033[32m8", "Delete all data linked to username\033[0m"],
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
        prices_dict = questions(USERNAME,None,prices)
        add_expenses(prices_dict)
    elif choice == 4:
        DATE = input_validator("date", "Please enter the date you want to update format YYYY-MM-DD")
        prices_dict = questions(USERNAME,DATE,prices)
        add_expenses(prices_dict)
    elif choice == 5:
        results = budget_overview(USERNAME)
        keys_list = list(prices.keys())
        print(tabulate(results, keys_list,"fancy_outline"))
        # Initialize a variable to store the sum of numbers
        total_sum = 0

        # Iterate through the inner lists
        for inner_list in results:
            # Slice the inner list from the 2nd element to the end to skip the first two strings
            numbers = inner_list[2:]
            # Using map() to convert strings to integers
            int_list = list(map(int, numbers))
            # Sum the numbers in the sliced list
            inner_sum = sum(int_list)

            # Add the inner sum to the total sum
            total_sum += inner_sum
        user_budget = get_budget(USERNAME)
        total_left = user_budget - total_sum
        print(tabulate([[user_budget,total_sum,total_left]],["Budget","Total spent","Saved"],"fancy_outline"))
    elif choice == 6:
        pass
    elif choice == 7:
        pass
    elif choice == 8:
        pass

