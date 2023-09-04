import gspread
from google.oauth2.service_account import Credentials
from print_input import input_validator,slow_print_effect

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
    SHEET = GSPREAD_CLIENT.open("budget-trainer")

    # get the income sheet
    INCOME_WORKSHEET = SHEET.worksheet("income")
    # gets the expenses sheet
    EXPENSES_WORKSHEET = SHEET.worksheet("expenses")

except FileNotFoundError: 
    print("Error: please try again")
except Exception as e:
    print(f"An error occurred: please refresh the browser")


def store_expenses(book):
     # Insert book to google sheets row
    EXPENSES_WORKSHEET.insert_row(book)

def store_Income(price):
    INCOME_WORKSHEET.insert_rows(price)

def search_woksheet(USERNAME):
    """search the google sheet by id's in the first column"""
    matching_cell = EXPENSES_WORKSHEET.find(USERNAME, in_column=1)
    user_row = EXPENSES_WORKSHEET.row_values(matching_cell.row)
    return user_row


def register():

    """"""   
    slow_print_effect("Please register!!\n enter your budget and Username, your username must be between 5 and 10 characters long")
    all_usernames = INCOME_WORKSHEET.col_values(1)
    BUDGET = input_validator("number", "Please Enter Your Budget: \n")
    while True:
        USERNAME = input_validator("username","please enter username?")

        if USERNAME in all_usernames:
            slow_print_effect(f"\033[34mPlease enter different username between 4 - 10 characters long!!\033[0m",0.005)    
            continue 
        else:
            slow_print_effect("Congradultion you are registered!!!")
            INCOME_WORKSHEET.append_row([USERNAME,BUDGET])
            break

        



