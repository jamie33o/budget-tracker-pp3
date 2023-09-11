from google_sheets import *
import unittest
from unittest.mock import patch,call,Mock

    
class TestGoogleSheets(unittest.TestCase):

    @patch('google_sheets.text_style')
    @patch('google_sheets.INCOME_WORKSHEET.col_values')
    @patch('google_sheets.slow_print_effect')
    @patch('google_sheets.input_validator')
    @patch('google_sheets.INCOME_WORKSHEET.append_row')
    def test_register_new_user(self, mock_append_row, mock_input_validator, mock_slow_print_effect, mock_col_values, mock_text_style):
        # Mock the Google Sheets API-related calls

        # Mock the return value of col_values to simulate the list of usernames
        mock_col_values.return_value = ["luke","dave"]

        # Mock the return values for input_validator, slow_print_effect, and text_style
        mock_input_validator.return_value = 500  # Simulate user input for budget  
        mock_text_style.side_effect = lambda style, text: text  # Mock text_style to return the second argument

        mock_slow_print_effect.side_effect = lambda x: None  # Mock the slow_print_effect

        # Call the register function
        result = register('jamie')

        # Assertions
        self.assertTrue(result)  # Expecting a new user to be added
        mock_col_values.assert_called_once_with(1)
        
        # Assert that text_style was called twice with specific arguments
        mock_text_style.assert_has_calls([
            call('info', "Please add your weekly budget as a whole number!! "),
            call('input', "Please Enter Your Budget: \n")
        ], any_order=True)
        
        mock_slow_print_effect.assert_called_once_with("Please add your weekly budget as a whole number!! ")
        mock_input_validator.assert_called_once_with("number", "Please Enter Your Budget: \n")
        mock_append_row.assert_called_once_with(['jamie', 500])



    @patch('google_sheets.INCOME_WORKSHEET.col_values')
    def test_login(self, mock_col_values):
        # Mock the Google Sheets API-related calls

        # Mock the return value of col_values to simulate usernames in income sheet
        mock_col_values.return_value = ["jamie","dave"]

        # Call the log in function
        result = login('jamie')

        # Assertions
        self.assertTrue(result)  # Expecting user to be logged in
        mock_col_values.assert_called_once_with(1)
        
    @patch('google_sheets.text_style')
    @patch('google_sheets.print')
    @patch('google_sheets.INCOME_WORKSHEET.find')
    def test_change_username_failed(self, mock_find_cell,mock_print, mock_text_style):
        # Mock the Google Sheets API-related calls

        # Mock the return value of find_cell to simulate username already exists
        mock_find_cell.return_value = True
        mock_text_style.return_value = "Please choose a different username\n"

        # Call the change username function
        result = change_username('jamie',"jamie33")

        # Assertions
        self.assertFalse(result)  # Expecting a new user to be added
        mock_find_cell.assert_called_once_with("jamie33", in_column=1)
    
        mock_print.assert_called_once_with("Please choose a different username\n")
        mock_text_style.assert_called_once_with("error","Please choose a different username\n")


    
    
    # patch function calls
    @patch('google_sheets.EXPENSES_WORKSHEET.update_acell')
    @patch('google_sheets.EXPENSES_WORKSHEET.findall')
    @patch('google_sheets.INCOME_WORKSHEET.update_acell')
    @patch('google_sheets.INCOME_WORKSHEET.find')
    def test_change_username_success(self, mock_find_cell,mock_income_update_acell,mock_findall,mock_expenses_update_acell):
        # Mock the Google Sheets API-related calls
    
        # Define the return values for two calls to the mocked find cell
        mock_find_cell.side_effect = [None,Mock(address='A4')]
        #return values for find all
        mock_findall.return_value = [Mock(address='A6'),Mock(address='A7')]
    

        # Call the change username function
        result = change_username('jamie',"jamie33")

        # Assertions
        self.assertTrue(result)  # Expecting username to be changed
        
        mock_find_cell.assert_has_calls([
            call("jamie33", in_column=1),
            call("jamie", in_column=1)
        ], any_order=False)        
        mock_income_update_acell.assert_called_once_with("A4", "jamie33")

        mock_findall.assert_called_once_with("jamie", in_column=1)


        mock_expenses_update_acell.assert_has_calls([
            call("A6", "jamie33"),
            call('A7', "jamie33")
        ], any_order=True)



if __name__ == '__main__':
    unittest.main()