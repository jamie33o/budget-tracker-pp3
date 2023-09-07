from print_input import slow_print_effect
from menu import menu
from print_input import input_validator


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
    Print logo.
    """
    slow_print_effect(f"\033[34m{LOGO}\033[0m",0.005)# ANSI escape codes to change the text color
    slow_print_effect("\nWelcome to Budget Trainer in this game you will train your memory to remember your budget and keep track of it\n")
    USERNAME = input_validator("username", "Please enter username,\n if you have used this website before please use the same username...\nIt must be 5 to 10 characters long")
    menu(USERNAME)


if __name__ == '__main__':
    main()
