import gspread
from google.oauth2.service_account import Credentials

# sets what im authorized to use with google cloud services
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]



# get the credentials from the config var
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# open the google sheets for budget trainer
SHEET = GSPREAD_CLIENT.open("budget-trainer")

# get the income sheet
INCOME = SHEET.worksheet("income")
# gets the expenses sheet
EXPENSES = SHEET.worksheet("expenses")


