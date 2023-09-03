import sys  # System-specific parameters and functions
import time  # provides functions for handling time-related tasks



def slow_print_effect(text, delay=0.04):
    """
    slow Typing effect for print statements
    """
    for letter in text:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(delay)


def input_validator(expected_type):
    input_value = ""
    if expected_type == "str":
        while True:
                input_value = input("\nType Y for yes and N for No (Y/N): \n")
                if input_value.upper() in ["Y", "N"]:
                       break  # Exit the loop if the input is a valid string
                else: 
                    slow_print_effect("Wrong input! Please enter text.")
    else:
        while True:
                try:
                    input_value = int(input("\nEnter the cost as a whole number: \n"))
                    break  # Exit the loop if the input is a valid integer
                except ValueError:
                    slow_print_effect("Wrong input! Please enter a whole number.")
    return input_value