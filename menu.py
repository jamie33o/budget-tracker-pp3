from print_input_effects import slow_print_effect


question_option_objects = {
    "question": {
        "Q1: How much does your daily commute cost?": "options":{"A. Walk or Bike", "B. Public Transport", "C. Car"},
        "Q2: How often do you eat out for lunch?": ["A. Never", "B. Rarely", "C. Occasionally"],
        "Q3: How often do you buy coffee or snacks?": ["A. Never", "B. Rarely", "C. Occasionally"],
        "Q4: How much do you spend on lunch daily?": ["A. $0-$5", "B. $6-$10", "C. $11-$15"],
    },
    "Staying at Home": {
        "Q1: Do you purchase groceries regularly?": ["A. Yes", "B. No"],
        "Q2: How much do you spend on groceries per week?": ["A. $0-$50", "B. $51-$100", "C. $101-$150"],
        "Q3: How often do you order food delivery?": ["A. Never", "B. Rarely", "C. Occasionally"],
    },
     "School": {
        "Q1: Do you purchase groceries regularly?": ["A. Yes", "B. No"],
        "Q2: How much do you spend on groceries per week?": ["A. $0-$50", "B. $51-$100", "C. $101-$150"],
        "Q3: How often do you order food delivery?": ["A. Never", "B. Rarely", "C. Occasionally"],
    }


}


def menu(question_option_objects):
    slow_print_effect(question_option_objects.question)
    for option in question_option_objects.options:
        slow_print_effect(option)
        choices = int(input("choose an option: "))

    return choices
