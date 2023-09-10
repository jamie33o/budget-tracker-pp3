import sys  # System-specific parameters and functions
import time  # provides functions for handling time-related tasks
import os
import re



def slow_print_effect(text, delay=0.04):
    """
    slow Typing effect for print statements
    """
    for letter in text:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(delay)


def input_validator(expected_type, input_text):
    """checks if input valid depending on expected type if its 
    string,date,username or int and returns the input if there is no error"""
    input_value = ""
    if expected_type == "letter":
        while True:
                input_value = input(f"\n {input_text}\n")
                input_value = input_value.upper()
                if input_value in ["Y", "N"]:
                       break  # Exit the loop if the input is a valid string
                else: 
                    slow_print_effect(text_style("error","Wrong input! Please enter text."))
    elif expected_type == "number":
        while True:
                try:
                    input_value = int(input(f"\n{input_text}\n"))
                    break  # Exit the loop if the input is a valid integer
                except ValueError:
                    slow_print_effect(text_style("error","Wrong input! Please enter a whole number."))
    elif expected_type == "username": 
        while True:
            input_value = input(text_style("input",f"\n{input_text}\n"))
            if len(input_value) in range(5,11):
                    break  # Exit the loop if the input is a valid username
            else: 
                slow_print_effect(text_style("error","Username must be between 6 to 11 characters"))
    elif expected_type == "date":
        while True:
            # Define the regular expression pattern for ISO date format (YYYY-MM-DD)
            iso_date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            input_value = input(f"\n{input_text}\n")
            # Check if the input matches the ISO date pattern
            if re.match(iso_date_pattern, input_value):
                break  # Input doesn't match the ISO format
            else: 
                slow_print_effect(text_style("error","Wrong input! Please enter date as YYYY-MM-DD."))
    return input_value


def text_style(type,message):
    if type == "success":
        styled_text = f"\033[32m{message}\033[0m"
    elif type == "error":
        styled_text = f"\033[31m{message}\033[0m"
    elif type == "info":
        styled_text = f"\033[33m{message}\033[0m"
    elif type == "input":
        styled_text = f"\033[36m\033[1m{message}\033[0m"


    return styled_text



def clear_terminal():
    """
    function to clear terminal
    """
    os.system('cls' if os.name == 'nt' else 'clear') 