import pyfiglet
from print_input import slow_print_effect,text_style
from menu import menu




def main():
    """
    Prints logo and welcome message then calls menu
    """

    logo = pyfiglet.figlet_format("Budget \n    Tracker", font = "digital")

    slow_print_effect(text_style("success",logo),0.005)# ANSI escape codes to change the text color
    slow_print_effect(text_style("info",
                                 """\nWelcome to Budget Tracker
                                 \nBudget Tracker helps you keep track of your budget\n"""))
    username = None
    while True:
        username = menu(username)

#  checks if the Python script is being run as the main program and not imported as a module
if __name__ == '__main__':
    main()
