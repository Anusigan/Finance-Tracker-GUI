#Importing json module to deal with data
import json

#Importing the 'main' function from the 'w2084774_part_C' module
from w2084774_part_C import main

#Global dictionary to store transactions
transactions = {}

#File handling functions
def load_transactions():
    """Function to load data from the JSON file transactions.json"""
    global transactions
    try:
        with open("transactions.json", "r") as file:
            transactions = json.load(file)
    except FileNotFoundError:
        """if such file is not found create an empty dictionery transactions"""
        transactions = {}

def save_transactions():
    """Function to create a JSON file transactions.json and save the transactions in dictionery to the JSON file"""
    global transactions
    with open("transactions.json", "w") as file:
        # Write the transactions dictionary to the file using json.dump()
        json.dump(transactions, file, indent=2)

def read_bulk_transactions_from_file(filename):
    """Function to read bulk transaction data from a text file and add them to the dictionery"""
    global transactions
    try:
        with open(filename, "r") as file:
            # Reading all the lines in the file
            lines = file.readlines()
            for line in lines:
                # Splitting each line 
                data = line.strip().split(",")
                # Checking the length of data to ensure all necessary data are present
                if len(data) == 4:
                    # Extracting transaction data from line
                    t_amount, t_category, t_type, t_date = map(str.strip, data)
                    
                    # Validate transaction amount in the text file
                    try:
                        t_amount = float(t_amount)
                    except ValueError:
                        # Printing an error message if the transaction amount is invalid
                        print(f"In {line.strip()}: {t_amount} is an invalid transaction amount. Transaction omitted.")
                        continue  # To skipping to the next iteration
                    
                    # Validate transaction type in the text file
                    if t_type.capitalize() != "Income" and t_type.capitalize()!= "Expense":
                        # Printing an error message if the transaction type is not (Income/Expense)
                        print(f"In {line.strip()}: {t_type} is an invalid transaction type. Transaction omitted.")
                        continue  # To skipping to the next iteration
                    
                    # Validating the transaction date format in the text file
                    if t_date[4]!="-" or t_date[7]!="-":   
                            #printing an error message if the transaction date is invalid 
                            print(f"In {line.strip()}: {t_date} is not in YYYY-MM-DD format. Transaction omitted." )
                            continue  #To skipping to the next itertion
                    
                    # Capitalizing the transaction categories in text file
                    t_category=t_category.capitalize()

                    # Adding the transactions to the global transactions dictionery having transaction category as key
                    if t_category in transactions:
                        transactions[t_category].append({"amount": t_amount, "type": t_type.capitalize(), "date": t_date})
                    else:
                        transactions[t_category] = [{"amount": t_amount, "type": t_type.capitalize(), "date": t_date}]
                        
                else:
                    # Printing an error message if the line does not have the necessary sufficient data  
                    print(f"In {line.strip()}: Transaction omitted due to insufficient data.")
            # Printing a success message after reading all transactions from the text file
            print("\nBulk transactions read from file successfully")
    except FileNotFoundError:
        # Printing an error message if the file is not found
        print("File is not found")
    # Saving the read bulk transactions to the JSON file
    save_transactions()



# Feature implementations
def add_transaction():
    """Function to add a transaction to the  dictionery"""
    global transactions
    t_amount = 0
    t_category = ""
    t_date = ""

    # Asking the transaction related details from the user as input
    while True:
        # Validating the transaction amount input
        try:
            t_amount = float(input("Enter the transaction amount: "))
            if t_amount <= 0:
                print("Amount must be a positive number. Please try again!")
            else:
                break
        except ValueError:
            # Printing an error message if the user does not give float value
            print("Invalid amount. Please try again!")

    while True:
        t_category = input("Enter the transaction category: ")
        t_category=t_category.capitalize()
        #Printing an error message if the user skip to give transaction category input
        if t_category == "":
            print("Transaction category can't be null. Please try again!")
        else:
            break
    # Validating the transaction type input
    while True:
        t_type=str(input("Enter the transaction type (Income/Expense): "))
        t_type=t_type.capitalize()
        # Checking whether user enters Income or Expense .If he enters something otherthan this notifying an error
        if t_type!="Income" and t_type!="Expense":
            print("Invalid input. Transaction type should be Income or Expense")
        else:
            break

    # Validating the transaction date input by checking whether it is in (YYYY-MM-DD) format
    while True:
        t_date = input("Enter the transaction date in YYYY-MM-DD format: ")
        if len(t_date) == 10:
            if t_date[4] == "-" and t_date[7] == "-":
                break
            else:
                print("Invalid input. Enter the date in YYYY-MM-DD format")
        else:
            print("Invalid input. Enter the date in YYYY-MM-DD format: ")

    # Creating a dictionary to store transaction data
    transaction = {"amount": t_amount, "type": t_type, "date": t_date}


    # Appending the transaction to the appropriate category in the transactions dictionery
    if t_category in transactions:
        transactions[t_category].append(transaction)
    else:
        transactions[t_category] = [transaction]

    # Saving the transactions to the JSON file
    save_transactions()

    # Printing a success message after transaction successfully added to the tracker
    print("Transaction added successfully to the tracker")

def view_transactions():
    """Function to display all the transactions categorized by category stored in dictionery"""
    global transactions
    if transactions:
        # Iterates all over each category and its transactions
        for category, category_data in transactions.items():
            # Printing the category name
            print(f"\nCategory: {category}")
            number=1
            # Iterating through each and every transaction in the specific category
            for transaction in category_data:
                # Printing the transaction details
                print(f"{number}. Transaction amount: {(transaction['amount'])}, Transaction type: {(transaction['type'])}, Transaction date: {transaction['date']}")
                number += 1
            
    else:
        # Printing a message if there is no transactions exists
        print("No transactions available")


def update_transaction():
    """Function to allow the user to update the existing added transactions"""
    global transactions

    """Calling the view transactions function to display the existing transactions to assist"""
    view_transactions()
    print("\n")

    # Checking whether transactions exists
    if transactions:
        # Asking for the category to be updated from the user
        category = input("Enter the transaction category to be updated: ")
        category=category.capitalize()

        # Checking whether that category exists
        if category in transactions:
            category_data = transactions[category]

            # Asking the user for transaction index to be updated
            while True:
                try:
                    number = int(input("Enter the transaction number to be updated: ")) - 1
                    if 0 <= number < len(category_data):
                        break
                    else:
                        # Printing an error message if the user enters a non existing index number 
                        print("Invalid transaction number. Please try again!")
                except:
                    # Printing an error message if the user enters invalid data type for transaction index number
                    print("Invalid input. Please try again!")
            
            # Asking updating transaction details form the user as input
            while True:
                # Asking and validating the transaction amount user enters
                try:
                    t_amount = float(input("Enter the new transaction amount: "))
                    if t_amount <= 0:
                        print("Amount must be a positive number. Please try again!")
                    else:
                        break
                except ValueError:
                    print("Invalid amount. Please try again!")

                
            while True:
                # Asking and validating the transaction type user enters
                t_type=str(input("Enter the transaction type (Income/Expense): "))
                t_type=t_type.capitalize()
                #Checking whether user enters Income or Expense .If he enters something otherthan this notifying an error
                if t_type!="Income" and t_type!="Expense":
                    print("Invalid input. Transaction type should be Income or Expense")
                else:
                    break

            while True:
                # Asking and validating the transaction date user enters
                t_date = input("Enter the new transaction date in YYYY-MM-DD format: ")
                if len(t_date) == 10:
                    if t_date[4] == "-" and t_date[7] == "-":
                        break
                    else:
                        print("Invalid input. Enter the date in YYYY-MM-DD format")
                else:
                    print("Invalid input. Enter the date in YYYY-MM-DD format: ")
            
            # Updating the new transaction details in the dictionery
            category_data[number]={"amount":t_amount, "type":t_type, "date":t_date}

            # Saving the updated transaction to the file
            save_transactions()

            # Printing a success message if transaction is successfully updated
            print("Transaction successfully updated")
        else:
            # Printing a message if the category user wants to update is not exists
            print("Category not found.")
    else:
        # Printing a message if there is no transactions present in that category for the user to update
        print("No transactions available in that category")

def delete_transaction():
    """Function to allow users to delete transactions present in the financial tracker"""

    global transactions

    # Calling the view transactions functions to display the transactions present
    view_transactions()
    print("\n")

    # Checking whether there are existing transactions
    if transactions:
        # Asking the user for the category where the transaction to be deleted is present
        category = input("Enter the category of the transaction to be deleted: ")
        category=category.capitalize()

        # Checking if that category exists
        if category in transactions:
            category_data= transactions[category]
            while True:
                # Asking and validating the  index number of the transaction to be deleted
                try:
                    number = int(input("Enter the transaction number to be deleted: ")) - 1
                    if 0 <= number< len(category_data):
                        break
                    else:
                        # Printing an error message if the input index number does not exist
                        print("Invalid Transaction number. Please try again!")
                except:
                    # Printing an error message if user input any other data typen instead of integer for transaction index number
                    print("Invalid input. Please try again!")

            # Delete the transaction 
            del category_data[number]

            # Removing the category if the category becomes empty after the transaction is deleted
            if len(category_data) == 0:  
                del transactions[category]

            # Saving the transaction to the JSON file 
            save_transactions()

            # Printing a success message if the transaction deleted successfully
            print("Transaction successfully deleted")
        else:
            # Printing a message if there are no transaction exist in the category user entered
            print("Category not found.")

def display_summary():
    """Function to calculate and display the summary of all transactions in the finance tracker"""
    global transactions
    total_income = 0
    total_expense = 0
    income_categories={}
    expense_categories={}

    # Iterating through the transactions and categorizing them to calculate summary
    for category, category_data in transactions.items():
        for transaction in category_data:
            
            if transaction['type'] == 'Income':
                total_income += transaction['amount']
                income_categories[category]=income_categories.get(category,0)+transaction["amount"]
            elif transaction['type'] == 'Expense':
                total_expense += transaction['amount']
                expense_categories[category]=expense_categories.get(category,0)+transaction["amount"]
    # Calculating the net value by subracting total expense from total income
    net_value = total_income - total_expense

    # Foramatting summary values
    total_income=(f"{total_income:.2f}")
    total_expense=(f"{total_expense:.2f}")
    net_value=(f"{net_value:.2f}")
    
    

    # Printing the summary of transactions
    head="TRANSACTIONS SUMMARY".center(50,".")
    print("\n",head)
    
    print("\nIncome Categories")
    print("--------------------")
    if income_categories:
        for category,amount in income_categories.items():
            print(f"{category}:{amount}")
    else:
        print("No income categories")

    
    print("\nExpense Categories")
    print("--------------------")
    if expense_categories:
        for category, amount in expense_categories.items():
            print(f"{category}:{amount}")
    else:
        print("No expense categories")
    
    print("\n******************************")
    print("Total Income:  ",total_income)
    print("Total Expense: ",total_expense)
    print("Net value:     ",net_value)
    print("******************************")
    

    
def main_menu():
    load_transactions()  
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. Read bulk transactions from a file")
        print("3. View Transactions")
        print("4. Update Transaction")
        print("5. Delete Transaction")
        print("6. Display Summary")
        print("7. Personal finance tracker GUI")
        print("8. Exit program")
        choice = input("\nEnter your choice: ")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            filename = input("Enter the file name to read bulk transaction: ")
            read_bulk_transactions_from_file(filename)
        elif choice == '3':
            view_transactions()
        elif choice == '4':
            update_transaction()
        elif choice == '5':
            delete_transaction()
        elif choice == '6':
            display_summary()
        elif choice == '7':
            main()
        elif choice == '8':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()

# if you are paid to do this assignment please delete this line of comment
