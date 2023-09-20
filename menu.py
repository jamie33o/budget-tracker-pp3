from tabulate import tabulate  # table prints
from print_input import (
     text_style,
     input_validator,
     slow_print_effect,
     clear_terminal
)
from questions import questions
from google_sheets import (
    delete_user,
    get_budget,
    register, login,
    budget_overview,
    change_budget,
    change_username,
    add_expenses
)


def menu(username):
    """main menu """
    input(text_style("input", "Press Enter to view the menu\n"))

    clear_terminal()

    expenses_dict = {  # dictionary matching google sheets expenses work sheet
        "username": username,
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
        "household": 0,
    }
    # check if user already logged in, otherwise show this menu
    if not username:
        username = login_or_register(expenses_dict, username)
        expenses_dict["username"] = username

    clear_terminal()

    menu_options = [  # main menu options list
        ["\033[36m",
            "***Budget Tracker Menu***\nPlease choose an option\033[0m"],
        ["1", "Change Username"],
        ["2", "Change Budget"],
        ["3", "Add/update today's expenses"],
        ["4", "Update expenses by date"],
        ["5", "View budget overview for previous 7 days from current date "],
        ["6", "View budget overview for previos 7 days from date entered"],
        ["7", "Delete all data linked to username"],
    ]
    keys_list = list(expenses_dict.keys())  # keys list of prices menu

    print(tabulate(menu_options))

    choice = input_validator("number",
                             "Please choose an option between 1 and 7:\n")

    # if/elif block to check which number the user entered
    if choice == 1:
        # User enters new username then it changes the username
        # matching current username to
        # new username in expenses and income worksheet
        while True:
            new_username = input_validator("username",
                                           "Please enter your new username,"
                                           "\nIt must be 5 to 10 characters"
                                           "long\n")
            username_changed = change_username(username, new_username)
            if username_changed:
                username = new_username
                slow_print_effect("success",
                                  "Username Updated!!!!\n")
                break
    elif choice == 2:
        # user enters there new budget then it is updated on income worksheet
        new_budget = input_validator("number",
                                     "Please enter your new budget: \n")

        budget_changed = change_budget(username, new_budget)

        if budget_changed:
            slow_print_effect("success",
                              "Budget Updated!!!!\n")
    elif choice == 3:
        update_user_expenses(expenses_dict, False)
    elif choice == 4:
        update_user_expenses(expenses_dict, True)
    elif choice == 5:
        view_budget_overview_by_date(username, keys_list, False,expenses_dict)
    elif choice == 6:
        view_budget_overview_by_date(username, keys_list, True,expenses_dict)
    elif choice == 7:
        username = delete_account(username)
    else:
        slow_print_effect("error",
                          f"{choice} is not an option!!!\n")
    return username


def sum_expenses(results, username):
    """Adds all the numbers in the reults list

    Parameters:
        USERNAME (string): users username
        results (list): list of numbers from expenses worksheet

    Returns:
        returns list: user budget from income worksheet,
                      result of adding all expenses, and ammount left
        """

    # Initialize a variable to store the sum of numbers
    total_sum = 0

    # Iterate through the inner lists
    for inner_list in results:
        # Slice the inner list from the 2nd element
        # to the end to skip the first two strings
        numbers = inner_list[2:]
        # Using map() to convert strings to integers
        int_list = list(map(int, numbers))
        # Sum the numbers in the sliced list
        inner_sum = sum(int_list)

        # Add the inner sum to the total sum
        total_sum += inner_sum
        user_budget = get_budget(username)
        total_left = user_budget - total_sum

    return [user_budget, total_sum, total_left]


def tabulate_data(results, keys_list, username):
    """Creates a styled table from data passed to it

    Parameters:
        USERNAME (string): users username
        results (list): list of number from expenses worksheet
        keys_list (list): list of strings from the prices dictionary keys
        """
    # list comprehension to remove first element and split the
    # second element of results which is the date
    # to just keep the day and store it in a new list
    new_results = [
        [inner_list[1].split("-")[2]] +
        inner_list[2:] if len(inner_list) > 1 else []
        for inner_list in results
    ]

    col1 = new_results
    col0 = keys_list[1:]
    # Print the table in columns
    table = list(zip(col0, *col1))

    # table format for column layout
    table_format = 'fancy_outline'

    # Print the table
    print(tabulate(table, tablefmt=table_format))
    total_expenses = sum_expenses(results, username)
    if total_expenses:
        print(tabulate([total_expenses],
                       ["Budget", "Total spent", "Saved"], "fancy_outline"))


def login_or_register(expenses_dict, username):
    """shows a menu for the user to log in or register

    Parameters:
        expenses_dict (dictionary): keys matching the
        fields in google expenses sheet
        """
    login_register_options = [
        ["1", "Log-in"],
        ["2", "Register"],
    ]

    print(tabulate(login_register_options))
    while True:
        # User chooses an option to login or register
        choice = input_validator("number", "Please choose an option")
        if choice in [1, 2]:
            break
        print(text_style("error", "Please enter 1 or 2\n"))
    while True:
        # user enter's a username for login or register
        username = input_validator("username",
                                   "Please enter a username"
                                   "\nIt must be 5 to 10 characters long")
        if choice == 1:
            # If user chose login it will check
            # if username is in income worksheet
            logged_in = login(username)
            if logged_in:
                slow_print_effect("success",
                                  "Congratulations you "
                                  "are logged in!!!\n")
                return username

            print(text_style("error",
                             f"{username} does not exist..."
                             "\nType 2 to register\nType 1 to try again\n"))
            # if username is not in the income worksheet the
            #  user can type 1 to try again or type 1 to register
            new_choice = input_validator("number",
                                         "Please choose an option")
            if new_choice == 2:
                choice = new_choice
            username = None
        else:
            # if the user chose register there
            # username will be added to income worksheet
            registered = register(username)
            if registered:
                slow_print_effect("success",
                                  "Congratulations you are registered!!!\n")
                # the user will be then asked to add expenses
                expenses_dict["username"] = username
                updated_expenses_dict = questions(None, expenses_dict)
                expenses_added = add_expenses(updated_expenses_dict)
                if expenses_added:
                    slow_print_effect("success", "Expenses Added!!!!\n")
                return username
            print(text_style("error",
                             "Error registering... Please try again...\n"))
            return None


def update_user_expenses(expenses_dict, update_by_date_bool):
    """
    if update_by_date_bool is true the user is asked to enter a
    date then the user is asked to add expenses and then
    expenses worksheet is updated for the date entered
    if update_by_date_bool is set to false expense
    are updated for the current date

    Parameters:
        expenses_dict(dictionary): keys matching the googlesheets
        expenses worksheet fields
        and the value will be the expenses the user adds

        update_by_date_bool(boolean): True: if the user can enter a
        date or False: use current date
    """

    if update_by_date_bool:
        date = input_validator("date",
                               "Please enter the date you want "
                               "to update, format: YYYY-MM-DD")
        updated_expenses_dict = questions(date, expenses_dict)
    else:
        updated_expenses_dict = questions(None, expenses_dict)
    expenses_added = add_expenses(updated_expenses_dict)
    if expenses_added:
        slow_print_effect("success", "Expenses Updated!!!!\n")


def view_budget_overview_by_date(username, keys_list, search_by_date_bool,expenses_dict):
    """
    if search_by_date_bool is true the user is asked to enter a date
    and the expenses are retrieved for the week before that date
    if it is false expenses are retrieved for the week before the current date

    Parameters:
        username (username): the username that the
        user enters on login or register
        keys_list(list): list of keys from the expenses_dict
        search_by_date_bool(boolean):  if true the user can
        get a budget overview by entering a date if false
        the budget overview will be from current date
    """
    if search_by_date_bool:
        date = input_validator("date",
                               "Please specify the end date of "
                               "the desired budget week ,"
                               "\nPlease enter the date format as YYYY-MM-DD")

        results = budget_overview(username, date)
    else:
        results = budget_overview(username, None)
    if results:
        tabulate_data(results, keys_list, username)
        update_single_expense(keys_list,results,expenses_dict)
    else:
        slow_print_effect("error",
                          "Sorry we have no expenses before that date!!!\n")


def delete_account(username):
    """
        User enters there username and if it matches the current
        username they are logged in with there account is deleted
    """
    username_to_delete = input_validator("username",
                                         "Please enter your username")
    if username == username_to_delete:
        ans = input_validator("letter",
                              "Are you sure you want to delete all data "
                              f"belonging to user {username_to_delete}?"
                              "\n Type Y for YES or N for NO (Y/N)")
        if ans == "Y":
            user_deleted = delete_user(username_to_delete)
            if user_deleted:
                slow_print_effect("success", "Account deleted!!!\n")
                return None

            slow_print_effect("error", "Account not deleted!!!\n")
        return username

    slow_print_effect("error", "Wrong Username!!!\n")
    return username


def update_single_expense(keys_list,results,expenses_dict):
    """
    Asks the user if they want to update a single expense then shows the user a list of
    the expenses and asks the user to choose which expense then asks the user to enter
    the date and amount to be updated with

    Parameters:
        keys_list (list): list of keys from expenses dictionary
        results(list): list of rows from the expenses worksheet
        expenses_dict(dictionary):  dictionary matching expenses worksheet columns
    """

    ans = input_validator("letter",
                            "Would you like to update any of these expenses?"
                            "\nY for yes and N for no (Y/N)")
    if ans == "Y":
        date = input_validator("date",
                                "Please enter date of expense you want to update?"
                                "\nPlease enter the date format as YYYY-MM-DD")
        # Assuming 'expenses' is a list of rows, and you want to update a 
        # row based on the 'date' condition
        expenses_row_to_update = [result for result in results if result[1] == date]
        if expenses_row_to_update:
            col0 = ["1","2","3","4","5","6","7","8","9","10"]
            col1 = keys_list[2:]
            # Print the table in columns
            table = list(zip(col0, col1))

            # table format for column layout
            table_format = 'fancy_outline'

            # Print the table
            print(tabulate(table, tablefmt=table_format))
            while True:
                expense_choice = input_validator("number",
                                            "Please choose the expense you want to update?")
                if str(expense_choice) in col0:
                    amount = input_validator("number",
                                            "Enter new amount for "
                                            f"{keys_list[expense_choice+1]} on {date}")
                    # Update the dictionary with values from the row
                    for i, key in enumerate(expenses_dict.keys()):
                        expenses_dict[key] = expenses_row_to_update[0][i]
                    expenses_dict[keys_list[expense_choice+1]] = amount
                    if add_expenses(expenses_dict):
                        slow_print_effect("success","Expense updated!!\n")
                    break
                print("Enter a number between 1 and 10")
                
        else:
            print(f"No rows matching this date: {date}")
