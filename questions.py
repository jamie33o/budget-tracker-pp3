from print_input import slow_print_effect,input_validator


def questions():


    prices = {# dictionary matching google sheets expenses work sheet
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


    questions_dict = { # dictionary with questions
        "Did you Work Today?": {"work-commute": "How much was your commute to work and home?", "work-lunch": "How much did you spend on lunch?"},
        "Did your kids go to school today?": {"kids-commute": "How much is there commute to school and home?", "kids-lunch": "How much did lunch's cost?"} ,
        "Did you go to school today?":{"adult-school-commute": "How much is your commute to school and home?", "adult-school-lunch":  "How much did lunch's cost?"} ,
        "Did you do Shopping today": {"shopping": "How much was your shoppimg?"},
        "Did you eat out today? e.g. Takeaway,resteraunt,drive through": {"eat-out": "How much did it cost?"},
        "Did you go to a shop for anything small today? e.g. snacks,coffe,tea,milk,bread etc...": {"small-shop-runs": "How much did it cost?"},
        "Did you pay any household bills today? e.g. gas, electricity, repairs" : {"household": "How much did it Cost?"}
    }


    for dict_key, dict_value in questions_dict.items():
        slow_print_effect(dict_key)
        ans = input_validator("str")
        if ans == "Y":
            if dict_value.items():
                for key, value in dict_value.items():
                        slow_print_effect(value)
                        cost = input_validator("number")
                        prices[key] = cost
            else:
                keys = list(dict_value.keys())  # Convert keys to a list
                key = keys[0]  # Access the first (and only) key in the list
                slow_print_effect(dict_value[key])
                cost = input_validator("number")
                prices[key] = cost


    return prices



