import gspread
from google.oauth2.service_account import Credentials
from print_input import input_validator,slow_print_effect
from datetime import datetime,timedelta


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
    print("Error: please try again")
except Exception as e:
    print(f"An error occurred: please refresh the browser")


def add_expenses(prices_dict):
    prices_list = list(prices_dict.values())

    matching_cells = EXPENSES_WORKSHEET.findall(prices_list[0], in_column=1)

    for cell in matching_cells:
        user_row = EXPENSES_WORKSHEET.row_values(cell.row)
    
        if prices_list[1] in user_row: 
            # delete row for that date if it excists
            EXPENSES_WORKSHEET.delete_row(cell.row)
            
    EXPENSES_WORKSHEET.append_row(prices_list)



def budget_overview(USERNAME):
    """search the google sheet and return budget"""
    user_rows = []    
    results = []
    current_date = datetime.now().date().isoformat()
    print(current_date)
    date1 = datetime.strptime(current_date, "%Y-%m-%d")
    
    matching_cells = EXPENSES_WORKSHEET.findall(USERNAME, in_column=1)
    for cell in matching_cells:
        user_rows.append(EXPENSES_WORKSHEET.row_values(cell.row))
    
    for row in user_rows:
        # Convert the date strings to datetime objects
        date2 = datetime.strptime(row[1], "%Y-%m-%d")
        # Calculate the difference between the two dates
        date_difference = date1 - date2
        # Check if the difference is less than 7 days
        if date_difference <= timedelta(days=7):
            results.append(row)

    return results

def change_username(USERNAME,NEW_USERNAME):
    try:
        matching_cell = INCOME_WORKSHEET.find(NEW_USERNAME, in_column=1)
        if matching_cell:
            print("Please choose a different username")
            return False
        else:
            matching_cell = INCOME_WORKSHEET.find(USERNAME, in_column=1)
            INCOME_WORKSHEET.update(matching_cell.address, NEW_USERNAME)

            matching_cells = EXPENSES_WORKSHEET.findall(USERNAME, in_column=1)

            # Update the username at each cell address
            for cell in matching_cells:
                EXPENSES_WORKSHEET.update_acell(cell.address, NEW_USERNAME)
            return True
    except FileNotFoundError: 
        print("Error changing username: please try again")
    except Exception as e:
        print(f"An error occurred: please try again")


def register(USERNAME):

    """"""   
    all_usernames = INCOME_WORKSHEET.col_values(1)
    if USERNAME not in all_usernames:
        slow_print_effect("Please add your weekly budget as a whole number!! ")
        BUDGET = input_validator("number", "Please Enter Your Budget: \n")
        slow_print_effect("Congradultion you are registered!!!")
        INCOME_WORKSHEET.append_row([USERNAME,BUDGET])
        EXPENSES_WORKSHEET.append_row([USERNAME])
        


def change_budget(USERNAME,NEW_BUDGET):
    matching_cell = INCOME_WORKSHEET.find(USERNAME, in_column=1)
    # Define the target column index (2 for column B)
    target_column_index = "B"
    # Calculate the A1 notation for the cell in the same row but in the target column
    target_cell_a1 = f"{target_column_index}{matching_cell.row}"

    # Update the username in the same row with the new username
    INCOME_WORKSHEET.update_acell(target_cell_a1,NEW_BUDGET)

def get_budget(USERNAME):
    matching_cell = INCOME_WORKSHEET.find(USERNAME, in_column=1)
    budget = INCOME_WORKSHEET.get(f"B{matching_cell.row}")
    
    int_budget = int(budget[0][0])
    return int_budget

