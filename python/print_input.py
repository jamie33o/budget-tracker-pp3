import sys  # System-specific parameters and functions
import time  # provides functions for handling time-related tasks
import os
import re


def slow_print_effect(msg_type, text, delay=0.04):
    """
    slow Typing effect for print statements
    """
    text = text_style(msg_type, text)

    for letter in text:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(delay)


def input_validator(expected_type, input_text):
    """checks if input is valid depending on expected type if its
    string,date,username or int and returns the input if there is no error

     Parameters:
        expected_type (string): the type of text input,
        letter, number, username, date
        input_text (string): the text to be validated

    Returns:
        returns input: The validated input
    """
    input_text = text_style("input", input_text)

    input_value = ""
    if expected_type == "letter":
        while True:
            input_value = input(f"\n {input_text}\n")
            input_value = input_value.upper()
            if input_value in ["Y", "N"]:
                break  # Exit the loop if the input is valid
            print(text_style("error", "Wrong input! Please enter text."))

    elif expected_type == "number":
        while True:
            try:
                input_value = int(input(f"\n{input_text}\n"))
                break  # Exit the loop if the input is a valid integer
            except ValueError:
                print(text_style("error",
                                 "Wrong input! Please enter a whole number."))

    elif expected_type == "username":
        while True:
            input_value = input(text_style("input", f"\n{input_text}\n"))
            if len(input_value) in range(5, 11):
                break  # Exit the loop if the input is a valid username
            print(text_style("error",
                             "Username must be between 6 to 11 characters"))

    elif expected_type == "date":
        while True:
            # Define the regular expression pattern
            # for ISO date format (YYYY-MM-DD)
            iso_date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            input_value = input(f"\n{input_text}\n")
            # Check if the input matches the ISO date pattern
            if re.match(iso_date_pattern, input_value):
                break  # Input doesn't match the ISO format
            print(text_style("error",
                             "Wrong input! Please enter date"
                             ", Format: YYYY-MM-DD."))

    return input_value


def text_style(msg_type, message):
    """Changes the style of text, color and weight

    Parameters:
        type (string): the type of text input, error, success, info
        message (string): the text to be styled

    Returns:
        returns styled_text: The text that has been styled
        """
    styled_text = ""
    if msg_type == "success":
        styled_text = f"\033[32m\033[1m{message}\033[0m"
    elif msg_type == "error":
        styled_text = f"\033[31m\033[1m{message}\033[0m"
    elif msg_type == "info":
        styled_text = f"\033[33m{message}\033[0m"
    elif msg_type == "input":
        styled_text = f"\033[36m\033[1m{message}\033[0m"

    return styled_text


def clear_terminal():
    """
    function to clear terminal
    """
    os.system('cls' if os.name == 'nt' else 'clear')
