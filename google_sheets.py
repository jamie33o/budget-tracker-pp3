import gspread
from google.oauth2.service_account import Credentials
from print_input import input_validator,slow_print_effect
from datetime import datetime,timedelta
from print_input import text_style


# sets what im authorized to use with google cloud services
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# try connect to google sheets if there is an error notify the user
try:
    # get the credentials from the config var
    CREDS = Credentials.from_service_account_file("creds.json")
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    # open the google sheets for budget trainer
    SHEET = GSPREAD_CLIENT.open("budget-tracker")

    # get the income sheet
    INCOME_WORKSHEET = SHEET.worksheet("income")
    # gets the expenses sheet
    EXPENSES_WORKSHEET = SHEET.worksheet("expenses")

except FileNotFoundError: 
    print("Error: please refresh the browser\n")
except Exception:
    print(f"An error occurred: please refresh the browser\n")


def register(USERNAME):
    """register's user by adding there user name and budget to goole sheet income worksheet
    and add username to expense worksheet
     Parameters:
        USERNAME (string): users username
        
    Returns:
        returns true or false: If user is added to worksheets"""   
    all_usernames = INCOME_WORKSHEET.col_values(1)
    if USERNAME not in all_usernames:
        slow_print_effect(text_style("info","Please add your weekly budget as a whole number!! "))
        BUDGET = input_validator("number", text_style("input","Please Enter Your Budget: \n"))
        INCOME_WORKSHEET.append_row([USERNAME,BUDGET])
        return True
    else:
        return False

def login(USERNAME):
    """log's the user in by checking if username exists 
   
    Parameters:
        USERNAME (string): users username
        
    Returns:
        returns true: If username is in worksheets
        returns false: If username is not in worksheets or if there is an error
        """    
    try:
        all_usernames = INCOME_WORKSHEET.col_values(1)
        if USERNAME in all_usernames:
            return True
        else:
            return False
    except Exception:
        print(text_style("error","Error logging in: please try again\n"))
        return False


def change_username(USERNAME,NEW_USERNAME):
    """changes the users username 

    Parameters:
        USERNAME (string): users username
        NEW_USERNAME (string): users new_username
        
    Returns:
        returns true: If username is changed
        returns false: If username is not changed
        """    
    try:
        matching_cell = INCOME_WORKSHEET.find(NEW_USERNAME, in_column=1)
        if matching_cell:
            print(text_style("error","Please choose a different username\n"))
            return False
        else:
            matching_cell = INCOME_WORKSHEET.find(USERNAME, in_column=1)
            INCOME_WORKSHEET.update_acell(matching_cell.address, NEW_USERNAME)

            matching_cells = EXPENSES_WORKSHEET.findall(USERNAME, in_column=1)

            # Update the username at each cell address
            for cell in matching_cells:
                EXPENSES_WORKSHEET.update_acell(cell.address, NEW_USERNAME)
            return True
    except Exception:
        print(text_style("error","Error changing username: please try again\n"))
        return False


def change_budget(USERNAME,NEW_BUDGET):
    """changes the users budget in the income worksheet 

    Parameters:
        USERNAME (string): users username
        NEW_BUDGET (string): users new_budget
        
    Returns:
        returns true: If budget is changed
        returns false: If budget is not changed
        """    
    try:
        matching_cell = INCOME_WORKSHEET.find(USERNAME, in_column=1)
        # Define the target column index (2 for column B)
        target_column_index = "B"
        # Calculate the A1 notation for the cell in the same row but in the target column
        target_cell_a1 = f"{target_column_index}{matching_cell.row}"

        # Update the username in the same row with the new username
        INCOME_WORKSHEET.update_acell(target_cell_a1,NEW_BUDGET)
        return True
    except Exception:
        print(text_style("error","Error changing budget: please try again\n"))
        return False




def add_expenses(prices_dict):
    """adds the users expenses to the expenses worksheet 

    Parameters:
        price_dict (dictionary): expenses dictionary
        
    Returns:
        returns true: If expenses are added to worksheet
        returns false: If expenses are not added
        """    
    prices_list = list(prices_dict.values())

    try:
        matching_cells = EXPENSES_WORKSHEET.findall(prices_list[0], in_column=1)

        for cell in matching_cells:
            user_row = EXPENSES_WORKSHEET.row_values(cell.row)
        
            if prices_list[1] in user_row: 
                # delete row for that date if it excists
                EXPENSES_WORKSHEET.delete_row(cell.row)
                
        EXPENSES_WORKSHEET.append_row(prices_list)
        return True
    except Exception:
        print(text_style("error","An error occurred while adding expenses"))
        return False

def budget_overview(USERNAME,DATE):
    """changes the users budget in the income worksheet 

    Parameters:
        USERNAME (string): users username
        DATE (string): user input date
        
    Returns:
        returns results: list of exspenses matching user user name with in 7days of current date
        or date input

        returns false: If there is an error
        """    
    user_rows = []    
    results = []
    try:
        if DATE:
            chosen_date = DATE
        else:
            chosen_date = datetime.now().date().isoformat()
        
        date1 = datetime.strptime(chosen_date, "%Y-%m-%d")
        
        matching_cells = EXPENSES_WORKSHEET.findall(USERNAME, in_column=1)
        for cell in matching_cells:
            user_rows.append(EXPENSES_WORKSHEET.row_values(cell.row))

        for row in user_rows:
            # Convert the date strings to datetime objects
            date2 = datetime.strptime(row[1], "%Y-%m-%d")
            # Calculate the difference between the two dates
            date_difference = date1 - date2
            # Check if the difference is less than 7 days
            if date_difference <= timedelta(days=7) and not date_difference < timedelta(days=0):
                results.append(row)

        return results
    except Exception:
        print(text_style("error","An error occurred while retrieving budget data"))
        return False


def delete_user(USERNAME):
    """deletes all data relating to the users username

    Parameters:
        USERNAME (string): users username
       
    Returns:
        returns true: if the data is deleted

        returns false: If there is an error
        """    
    try:
        matching_cell = INCOME_WORKSHEET.find(USERNAME, in_column=1)
        matching_cells = EXPENSES_WORKSHEET.findall(USERNAME, in_column=1)
        INCOME_WORKSHEET.delete_row(matching_cell.row)

        for cell in matching_cells:
            EXPENSES_WORKSHEET.delete_row(cell.row)
    except Exception:
        print(text_style("error","Error deleting data please try again"))
        


def get_budget(USERNAME):
    """retrieves the users budget

    Parameters:
        USERNAME (string): users username
       
    Returns:
        returns true: if the budget is retrieved
        returns false: If there is an error
        """    
    try:
        matching_cell = INCOME_WORKSHEET.find(USERNAME, in_column=1)
        budget = INCOME_WORKSHEET.get(f"B{matching_cell.row}")
        int_budget = int(budget[0][0])
        return int_budget
    except Exception:
        print(text_style("error","Error retrieving budget"))
        return False


