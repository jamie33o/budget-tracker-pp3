from tabulate import tabulate  # table prints
from print_input import *
from questions import questions
from google_sheets import *

USERNAME = None


def menu():
    
    input(text_style("input","Press Enter to view the menu"))
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
            ["1" , "Log-in"],
            ["2", "Register"],
        ]
        
        print(tabulate(login_register_options)) 
        while True:
            choice = input_validator("number", text_style("input","Please choose an option"))
            if choice in [1,2]:
                break
            else:
                print(text_style("error","Please enter 1 or 2\n"))
        while True:
            USERNAME = input_validator("username", text_style("input","Please enter a username\nIt must be 5 to 10 characters long"))
            if choice == 1:
                logged_in = login(USERNAME)
                if logged_in:
                    slow_print_effect(text_style("success","Congradultion you are logged in!!!\n"))
                    break
                else:
                    print(text_style("error",f"{USERNAME} does not exist... \nType 1 to register\nType 2 to try again\n"))
                    new_choice = input_validator("number", text_style("input","Please choose an option"))
                    if new_choice == 1:
                        choice = new_choice
                    USERNAME = None
            else:
                registered = register(USERNAME)
                if registered:
                    slow_print_effect(text_style("success","Congradultion you are registered!!!\n"))
                    prices["username"] = USERNAME
                    prices_dict = questions(None,prices)
                    expenses_added = add_expenses(prices_dict)
                    if expenses_added:
                        slow_print_effect(text_style("success","Expenses Added!!!!\n"))
                    break
                else:
                    print(text_style("error","Error registering... Please try again...\n"))
                    USERNAME = None
            
    clear_terminal()

    menu_options = [
        ["\033[36m" , "***Budget Tracker Menu***\nPlease choose an option\033[0m"],
        ["1", "Change Username"],
        ["2", "Change Budget"],
        ["3", "Add/update today's expenses"],
        ["4", "Update expenses by date"],
        ["5", "View budget overview for last 7 days"],
        ["6", "Search budget overview by date"],
        ["7", "Delete all data linked to username"],
    ]
    keys_list = list(prices.keys())

    print(tabulate(menu_options))

    choice = input_validator("number",text_style("input", "Please choose an option between 1 and 7:\n"))


    if choice == 1:
        while True:
            NEW_USERNAME = input_validator("username",text_style("input", """Please enter your new username,
                    \nIt must be 5 to 10 characters long\n"""))
            username_changed = change_username(USERNAME,NEW_USERNAME)
            if username_changed:
                USERNAME = NEW_USERNAME
                slow_print_effect(text_style("input","Username Updated!!!!\n"))
                break
            
    elif choice == 2:
        NEW_BUDGET = input_validator("number", text_style("input", "Please enter your new budget: \n"))
        budget_changed = change_budget(USERNAME ,NEW_BUDGET)
        if budget_changed:
            slow_print_effect(text_style("success","Budget Updated!!!!\n"))
    elif choice == 3:
        prices_dict = questions(None,prices)
        expenses_added = add_expenses(prices_dict)
        if expenses_added:
            slow_print_effect(text_style("success","Expenses Added!!!!\n"))
    elif choice == 4:
        DATE = input_validator("date", text_style("input","Please enter the date you want to update format YYYY-MM-DD"))
        prices_dict = questions(DATE,prices)
        expenses_added = add_expenses(prices_dict)
        if expenses_added:
            slow_print_effect(text_style("success","Expenses Updated!!!!\n"))
    elif choice == 5:
        results = budget_overview(USERNAME,None)
        if results :
            tabulate_data(results,keys_list,USERNAME)
        else:
            slow_print_effect(text_style("error","Sorry you have no expenses added!!!\n"))

    elif choice == 6:
        date = input_validator("date", text_style("input","Please enter the date for the budget, which will be 7 days previous to the date you provide.\nPlease enter date as YYYY-MM-DD"))
        results = budget_overview(USERNAME,date)
        if results:
            tabulate_data(results,keys_list,USERNAME)
        else:
            slow_print_effect(text_style("error","Sorry we have no expenses before that date!!!\n"))

    elif choice == 7:
        USERNAME_TO_DELETE = input_validator("username",text_style("input","Please enter your username"))
        if USERNAME == USERNAME_TO_DELETE:
            ans = input_validator("letter",text_style("input",f"Are you sure you want to delete all data belonging to user {USERNAME_TO_DELETE}?\n Type Y for YES and N for NO (Y/N)"))
            if ans == "Y":
                user_deleted = delete_user(USERNAME_TO_DELETE)
                if user_deleted:
                    slow_print_effect(text_style("success","Account deleted!!!\n"))
                    USERNAME = None
        else:
            slow_print_effect(text_style("error","Wrong Username!!!\n"))
    else:
        slow_print_effect(text_style("error",f"{choice} is not an option!!!\n"))



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
    col0 = keys_list
    # Print the table in columns
    table = list(zip(col0, *col1))

    # Use a suitable table format for column layout (e.g., 'plain', 'simple', 'pipe', 'orgtbl')
    table_format = 'fancy_outline'

    # Print the table
    print(tabulate(table, tablefmt=table_format))
    total_expenses = sum_expenses(results,USERNAME)
    if total_expenses:
        print(tabulate([total_expenses],["Budget","Total spent","Saved"],"fancy_outline"))