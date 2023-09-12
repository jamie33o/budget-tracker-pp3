from print_input import slow_print_effect,text_style
from menu import menu


LOGO = """
 
 /$$$$$$$                  /$$                       /$$                     
| $$__  $$                | $$                      | $$                     
| $$  \ $$ /$$   /$$  /$$$$$$$  /$$$$$$   /$$$$$$  /$$$$$$                   
| $$$$$$$ | $$  | $$ /$$__  $$ /$$__  $$ /$$__  $$|_  $$_/                   
| $$__  $$| $$  | $$| $$  | $$| $$  \ $$| $$$$$$$$  | $$                     
| $$  \ $$| $$  | $$| $$  | $$| $$  | $$| $$_____/  | $$ /$$                 
| $$$$$$$/|  $$$$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$$  |  $$$$/                 
|_______/  \______/  \_______/ \____  $$ \_______/   \___/                   
                               /$$  \ $$                                     
            /$$$$$$$$         |  $$$$$$/        /$$                          
           |__  $$__/          \______/        | $$                          
              | $$  /$$$$$$  /$$$$$$   /$$$$$$$| $$   /$$  /$$$$$$   /$$$$$$ 
              | $$ /$$__  $$|____  $$ /$$_____/| $$  /$$/ /$$__  $$ /$$__  $$
              | $$| $$  \__/ /$$$$$$$| $$      | $$$$$$/ | $$$$$$$$| $$  \__/
              | $$| $$      /$$__  $$| $$      | $$_  $$ | $$_____/| $$      
              | $$| $$     |  $$$$$$$|  $$$$$$$| $$ \  $$|  $$$$$$$| $$      
              |__/|__/      \_______/ \_______/|__/  \__/ \_______/|__/                                            
"""


def main():
    """
    Prints logo and welcome message then calls menu
    """
    slow_print_effect(text_style("success",LOGO),0.005)# ANSI escape codes to change the text color
    slow_print_effect(text_style("info",
                                 """\nWelcome to Budget Tracker
                                 \nBudget Tracker helps you keep track of your budget\n"""))
    while True:
        menu()

#  checks if the Python script is being run as the main program and not imported as a module
if __name__ == '__main__':
    main()
