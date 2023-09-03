import sys  # System-specific parameters and functions
import time  # provides functions for handling time-related tasks



def slow_print_effect(text, delay=0.08):
    """
    slow Typing effect for print statements
    """
    for letter in text:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(delay)
