from tabulate import tabulate  # table prints
from print_input import input_validator,clear_terminal
from questions import questions
from google_sheets import *

USERNAME = None


def menu():
    
    input("Press Enter to view the menu\n")
    global USERNAME
    clear_terminal()

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
    
    if not USERNAME:
        login_register_options = [
            ["\033[32m1" , "Log-in\033[0m"],
            ["\033[32m2", "Register\033[0m"],
        ]
        
        print(tabulate(login_register_options)) 

        choice = input_validator("number", "Please choose an option")
        
        while True:
            USERNAME = input_validator("username", "Please enter username\nIt must be 5 to 10 characters long")
            if choice == 1:
                logged_in = login(USERNAME)
                if logged_in:
                    slow_print_effect("Congradultion you are logged in!!!\n")
                    break
                else:
                    print("Error logging in... Please try again...\n")
                    USERNAME = None
            else:
                registered = register(USERNAME)
                if registered:
                    slow_print_effect("Congradultion you are registered!!!\n")
                    prices["username"] = USERNAME
                    prices_dict = questions(None,prices)
                    expenses_added = add_expenses(prices_dict)
                    if expenses_added:
                        slow_print_effect("Expenses Added!!!!\n")
                    break
                else:
                    print("Error registering... Please try again...\n")
                    USERNAME = None
            
   
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

    choice = input_validator("number","Please choose an option between 1 and 5:\n")


    if choice == 1:
        while True:
            NEW_USERNAME = input_validator("username","""Please enter your new username,
                    \nIt must be 5 to 10 characters long\n""")
            username_changed = change_username(USERNAME,NEW_USERNAME)
            if username_changed:
                USERNAME = NEW_USERNAME
                slow_print_effect("Username Updated!!!!\n")
                menu()
                break
            
    elif choice == 2:
        NEW_BUDGET = input_validator("number", "Please enter your new budget: \n")
        budget_changed = change_budget(USERNAME ,NEW_BUDGET)
        if budget_changed:
            slow_print_effect("Budget Updated!!!!\n")
        menu()
    elif choice == 3:
        prices_dict = questions(None,prices)
        expenses_added = add_expenses(prices_dict)
        if expenses_added:
            slow_print_effect("Expenses Added!!!!\n")
        menu()
    elif choice == 4:
        DATE = input_validator("date", "Please enter the date you want to update format YYYY-MM-DD")
        prices_dict = questions(DATE,prices)
        expenses_added = add_expenses(prices_dict)
        if expenses_added:
            slow_print_effect("Expenses Updated!!!!\n")
        menu()
    elif choice == 5:
        results = budget_overview(USERNAME,None)
        if results :
            tabulate_data(results,keys_list,USERNAME)
        menu()
    elif choice == 6:
        date = input_validator("date", "Please enter the date that you want 7 day budget from")
        results = budget_overview(USERNAME,date)
        if len(results) >5:
            tabulate_data(results,keys_list,USERNAME)
        menu()
    elif choice == 7:
        USERNAME_TO_DELETE = input_validator("username","Please enter your username")
        ans = input_validator("letter",f"Are you sure you want to delete all data belonging to user {USERNAME_TO_DELETE}?\n Type Y for YES and N for NO (Y/N)")
        if ans == "Y":
            user_deleted = delete_user(USERNAME_TO_DELETE)
            if user_deleted:
                slow_print_effect("Account deleted!!!")
                USERNAME = None
            menu()
        else:
            menu()


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


def tabulate_data(results,keys_list,USERNAME):
    col1 = results
    col0=keys_list
    # Print the table in columns
    table = list(zip(col0, *col1))

    # Use a suitable table format for column layout (e.g., 'plain', 'simple', 'pipe', 'orgtbl')
    table_format = 'fancy_outline'

    # Print the table
    print(tabulate(table, tablefmt=table_format))
    total_expenses = sum_expenses(results,USERNAME)
    if total_expenses:
        print(tabulate([total_expenses],["Budget","Total spent","Saved"],"fancy_outline"))