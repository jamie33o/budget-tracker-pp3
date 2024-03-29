from datetime import datetime
from python.print_input import slow_print_effect,input_validator,text_style

def questions(date,expenses_dict):
    """
    prints the questions in the dictionary based on the users input and then takes the number input 
    and adds it to the expenses_dict dictionary

    Parameters:
        date(string): user inputs a date
        expenses_dict(dictionary): expenses dictionary
    Return:
        returns the updated expenses_dict
    """
    slow_print_effect("info","Please add your expenses\n")

    if date:
        current_date = date
    else:
        current_date = datetime.now().date().isoformat()# turn date object to ISO format

    expenses_dict["date"] = current_date

    questions_dict = { # dictionary with the questions
        "Did you Work Today?": 
        {"work-commute": "How much was your commute to work and home?",
          "work-lunch": "How much did you spend on lunch?"},

        "Did your kids go to school today?": 
        {"kids-commute": "How much is there commute to school and home?",
         "kids-lunch": "How much did lunch's cost?"} ,

        "Did you go to school today?":
        {"adult-school-commute": "How much is your commute to school and home?",
         "adult-school-lunch":  "How much did lunch's cost?"},

        "Did you do Shopping today": 
        {"shopping": "How much was your shoppimg?"},

        "Did you eat out today? e.g. Takeaway,resteraunt,drive through": 
        {"eat-out": "How much did it cost?"},

        "Did you go to a shop for anything small today? e.g. snacks,coffe,tea,milk,bread etc...": 
        {"small-shop-runs": "How much did it cost?"},

        "Did you pay any household bills today? e.g. gas, electricity, repairs" : 
        {"household": "How much did it Cost?"}
    }


    for dict_key, dict_value in questions_dict.items():
        # goes through question's in the dictionary depending on user input
        # and ask for cost as input and adds it to the expenses dictionary
        slow_print_effect("info", dict_key)
        ans = input_validator("letter","Type Y for yes and N for No (Y/N):")
        if ans == "Y":
            if dict_value.items():
                for key, value in dict_value.items():
                    slow_print_effect("info",value)
                    cost = input_validator("number","Enter the cost as a whole number: ")
                    expenses_dict[key] = cost
            else:
                keys = list(dict_value.keys())  # Convert keys to a list
                key = keys[0]  # Access the first (and only) key in the list
                slow_print_effect("info",dict_value[key])
                cost = input_validator("number","Enter the cost as a whole number: " )
                expenses_dict[key] = cost


    return expenses_dict
