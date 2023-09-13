import pyfiglet
from print_input import slow_print_effect
from menu import menu


def main():
    """
    Prints logo and welcome message then calls menu
    """

    logo = pyfiglet.figlet_format("Budget \n    Tracker", font="digital")
    # ANSI escape codes to change the text color
    slow_print_effect("success", logo, 0.05)
    slow_print_effect("info",
                      "Welcome to Budget Tracker,"
                      "\nYour personal budget management tool.\n"
                      "Budget Tracker is here to help you keep "
                      "a close eye on your finances.\n")
    username = None
    while True:
        username = menu(username)


#  checks if the Python script is being run
# as the main program and not imported as a module
if __name__ == '__main__':
    main()
