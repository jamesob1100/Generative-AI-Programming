"""
#data generator function
#function header
    The Data Generator Function creates random numerical or categorical data in csv format 
    based on what the user asks for such as entering ‘circle’, ‘square’, ‘triangle’ for categorical 
    columns and sizes for numerical columns.

    parameters:
    num_rows (int): The number of rows of data to generate.
    num_cols (int): The number of columns of data to generate.
    col_types (list): A list of strings specifying the type of each column ('numerical' or 'categorical').
    categorical_options (list): A list of lists, where each inner list contains the possible categorical values for the corresponding categorical column.

    returns:
    list: A list of lists representing the generated data, where each inner list corresponds to a row of data.

#file function
#function header
    The File Function will open/create a file based on the inputted file name given by the user, 
    it then saves the data generated into the opened/created file.

    parameters:
    filename (str): The name of the file to save the generated data to.
    data (list): A list of lists representing the generated data to be saved, 
    where each inner list corresponds to a row of data.

    returns:
    None: This function does not return any value, it simply writes the data to the specified file.

#main function
#function header
    1.  User is prompted to enter number of data points to generate or cancel
    2.  User enters integer value of number of data points
    3.  User is prompted to either enter column name which starts with a letter and ends   with a letter or cancel the creation
    4.  User enters column name
    5. User is prompted to enter the data type generated in the column, either categorical or numerical, or cancel
    6. User enters categorical data type
    7. User is prompted to enter a list of strings of categories to fill the column (e.g. ‘circle’, ‘square’, ‘red’, ‘blue’ etc.) or cancel
    8. User enters minimum of one string
    9. Program returns to step 3
    ---
    6a. User enters numerical data type
    7a. User is prompted to provide two integers to define the range of created data (e.g. 2 5   == generate values between 2 and 5)
    8a. User enters two numbers
    9a. Program returns to step 3
    ---
    4b. User selects cancel/finish creation
    5b. User is prompted to enter a file name to save this data to, if no such file exists one is created
    6b. User enters file name
    7b. data is saved to the file and program terminates
    ---
    5c. User enters cancel 
    6c. Return to step 3
    ---
    8d. User enters cancel
    9d. Return to step 5
    ---
    2e. User selects cancel
    3e.  Program terminates
    ---
    2f. User enters non-integer
    3f. User is given an error and returned to 1
    4f. User enters invalid column name
    5f. User is given an error and returned to 3
    ---
    6g. User enters invalid data type
    7g. User is given an error and returned to 5
    ---
    8h. User enters invalid string/integer
    9h. User is given an error and returned to 7 

    parameters:
    None: This function does not take any parameters, it interacts with the user through prompts and generates data based on the user's input.

    returns:
    None: This function does not return any value, it generates data and saves it to a file based on user input, and then terminates.
"""
import random
import csv

def data_generator(num_rows, num_cols, col_types, categorical_options):
    data = []
    for _ in range(num_rows):
        row = []
        for col_type, options in zip(col_types, categorical_options):
            if col_type == 'numerical':
                row.append(random.randint(options[0], options[1]))
            elif col_type == 'categorical':
                row.append(random.choice(options))
        data.append(row)
    return data

def save_to_file(filename, data):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def main():
    while True:
        num_rows = input("Enter the number of data points to generate (or 'cancel' to exit): ")
        if num_rows.lower() == 'cancel':
            print("Program terminated.")
            return
        if not num_rows.isdigit():
            print("Invalid input. Please enter an integer.")
            continue
        num_rows = int(num_rows)

        col_types = []
        categorical_options = []
        while True:
            col_name = input("Enter column name (or 'cancel' to finish): ")
            if col_name.lower() == 'cancel':
                break
            if not (col_name[0].isalpha() and col_name[-1].isalpha()):
                print("Invalid column name. It must start and end with a letter.")
                continue

            data_type = input("Enter data type for the column (categorical/numerical) or 'cancel' to finish: ")
            if data_type.lower() == 'cancel':
                break
            if data_type.lower() not in ['categorical', 'numerical']:
                print("Invalid data type. Please enter 'categorical' or 'numerical'.")
                continue

            col_types.append(data_type.lower())
            if data_type.lower() == 'categorical':
                options = input("Enter a list of categories for this column (comma separated) or 'cancel' to finish: ")
                if options.lower() == 'cancel':
                    break
                categorical_options.append(options.split(','))
            else:
                range_input = input("Enter the range for numerical data (e.g. 2 5) or 'cancel' to finish: ")
                if range_input.lower() == 'cancel':
                    break
                try:
                    min_val, max_val = map(int, range_input.split())
                    categorical_options.append((min_val, max_val))
                except ValueError:
                    print("Invalid range. Please enter two integers separated by a space.")
                    continue

        filename = input("Enter a file name to save the generated data (or 'cancel' to exit): ")
        if filename.lower() == 'cancel':
            print("Program terminated.")
            return

        data = data_generator(num_rows, len(col_types), col_types, categorical_options)
        save_to_file(filename, data)
        print(f"Data saved to {filename}. Program terminated.")
        return
    
if __name__ == "__main__":
    main()