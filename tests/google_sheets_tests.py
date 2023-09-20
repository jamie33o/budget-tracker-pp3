import unittest
from unittest.mock import patch, call, Mock
from python.google_sheets import login, register, change_username


class TestGoogleSheets(unittest.TestCase):
    """
    Test class for testing functions in google_sheets.py
    """

    
    @patch('python.google_sheets.INCOME_WORKSHEET.col_values')
    @patch('python.google_sheets.slow_print_effect')
    @patch('python.google_sheets.input_validator')
    @patch('python.google_sheets.INCOME_WORKSHEET.append_row')
    def test_register_new_user(self,
                               mock_append_row,
                               mock_input_validator,
                               mock_slow_print_effect,
                               mock_col_values):

        """
        Test for register function in google_sheets.py
        """
        # Mock the Google Sheets API-related calls

        # Mock the return value of col_values to simulate the list of usernames
        mock_col_values.return_value = ["luke", "dave"]

        # Mock the return values for input_validator,
        # slow_print_effect, and text_style

        # Simulate user input for budget
        mock_input_validator.return_value = 500
        # Mock the slow_print_effect
        mock_slow_print_effect.side_effect = lambda x, y=None: None

        # Call the register function
        result = register('jamie')

        # Assertions
        self.assertTrue(result)  # Expecting a new user to be added
        mock_col_values.assert_called_once_with(1)

        mock_slow_print_effect.assert_called_once_with("info",
            "Please add your weekly budget as a whole number!!")
        mock_input_validator.assert_called_once_with(
                                            "number",
                                            "Please Enter Your Budget: \n")
        mock_append_row.assert_called_once_with(['jamie', 500])


    @patch('python.google_sheets.INCOME_WORKSHEET.col_values')
    def test_login(self, mock_col_values):
        """
        Test for login function in google_sheets.py
        """
        # Mock the Google Sheets API-related calls

        # Mock the return value of col_values
        # to simulate usernames in income sheet
        mock_col_values.return_value = ["jamie", "dave"]

        # Call the log in function
        result = login('jamie')

        # Assertions
        self.assertTrue(result)  # Expecting user to be logged in
        mock_col_values.assert_called_once_with(1)


    @patch('python.google_sheets.text_style')
    @patch('python.google_sheets.print')
    @patch('python.google_sheets.INCOME_WORKSHEET.find')
    def test_change_username_failed(self,
                                    mock_find_cell,
                                    mock_print,
                                    mock_text_style):
        """
        Test function for change username function in google sheets
        change username test fail condition
        """
        # Mock the Google Sheets API-related calls

        # Mock the return value of find_cell to
        # simulate username already exists
        mock_find_cell.return_value = True
        mock_text_style.return_value = "Please choose a different username\n"

        # Call the change username function
        result = change_username('jamie', "jamie33")

        # Assertions
        self.assertFalse(result)  # Expecting a new user to be added
        mock_find_cell.assert_called_once_with("jamie33", in_column=1)

        mock_print.assert_called_once_with(
                "Please choose a different username\n")

        mock_text_style.assert_called_once_with(
                "error",
                "Please choose a different username\n")

    # patch function calls
    @patch('python.google_sheets.EXPENSES_WORKSHEET.update_acell')
    @patch('python.google_sheets.EXPENSES_WORKSHEET.findall')
    @patch('python.google_sheets.INCOME_WORKSHEET.update_acell')
    @patch('python.google_sheets.INCOME_WORKSHEET.find')
    def test_change_username_success(self,
                                     mock_find_cell,
                                     mock_income_update_acell,
                                     mock_findall,
                                     mock_expenses_update_acell):
        """
        Test for the username function in google sheetes
        success condition
        """
        # Mock the Google Sheets API-related calls

        # Define the return values for two calls to the mocked find cell
        mock_find_cell.side_effect = [None, Mock(address='A4')]
        # return values for find all
        mock_findall.return_value = [Mock(address='A6'), Mock(address='A7')]

        # Call the change username function
        result = change_username('jamie', "jamie33")

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
