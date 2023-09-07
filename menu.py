from tabulate import tabulate  # table prints
from print_input import input_validator,clear_terminal
from questions import questions
from google_sheets import *


def menu(USERNAME):
    
    input("Press Enter to view the menu")

    clear_terminal()

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
        ["\033[32m5", "View budget overview for last 7 days \033[0m"],
        ["\033[32m6", "Search budget overview by date\033[0m"],
        ["\033[32m7", "Delete all data linked to username\033[0m"],
    ]
    keys_list = list(prices.keys())

    print(tabulate(menu_options))

    choice = input_validator("number","Please choose an option between 1 and 5")


    if choice == 1:
        while True:
            NEW_USERNAME = input_validator("username",""" Please enter your new username,
                \nIt must be 5 to 10 characters long""")
            username_changed = change_username(USERNAME,NEW_USERNAME)
            if username_changed:
                USERNAME = NEW_USERNAME
                break
        
        slow_print_effect("Username Updated!!!!")
        menu(USERNAME)
    elif choice == 2:
        NEW_BUDGET = input_validator("number", "Please enter your new budget:")
        change_budget(USERNAME ,NEW_BUDGET) 
        slow_print_effect("Budget Updated!!!!")
        menu(USERNAME)
    elif choice == 3:
        prices_dict = questions(None,prices)
        add_expenses(prices_dict)
        
        slow_print_effect("Expenses Added!!!!")
        menu(USERNAME)
    elif choice == 4:
        DATE = input_validator("date", "Please enter the date you want to update format YYYY-MM-DD")
        prices_dict = questions(DATE,prices)
        add_expenses(prices_dict)
        
        slow_print_effect("Expenses Updated!!!!")
        menu(USERNAME)
    elif choice == 5:
        results = budget_overview(USERNAME,None)
        print(tabulate(results, keys_list))
        total_expenses = sum_expenses(results,USERNAME)
        print(tabulate([total_expenses],["Budget","Total spent","Saved"],"fancy_outline"))
        menu(USERNAME)
    elif choice == 6:
        date = input_validator("date", "Please enter the date that you want 7 day budget from")
        results = budget_overview(USERNAME,date)
        print(tabulate(results, keys_list,"fancy_outline"))
        total_expenses = sum_expenses(results,USERNAME)
        print(tabulate([total_expenses],["Budget","Total spent","Saved"],"fancy_outline"))

        menu(USERNAME)

    elif choice == 7:
        USERNAME_TO_DELETE = input_validator("username","Please enter your username")
        ans = input_validator("letter",f"Are you sure you want to delete all data belonging to user {USERNAME_TO_DELETE}?\n Type Y for YES and N for NO (Y/N)")
        if ans == "Y":
            delete_user(USERNAME_TO_DELETE)
            slow_print_effect("Account deleted!!!")
            menu(None)
        else:
            menu(USERNAME)


def sum_expenses(results,USERNAME):
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

    return [user_budget,total_sum,total_left]