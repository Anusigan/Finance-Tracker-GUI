#Importing tkinter module to create GUI and ttk for styling and importing json module to load transactions 
import tkinter as tk
from tkinter import ttk
import json

#Defining a class for finance tracker graphical user interface
class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.create_widgets()
        self.transactions = self.load_transactions("transactions.json")

    def create_widgets(self):
        """Method to create widgets for the GUI"""
        
        #Frame for table and scrollbar
        #Window Size initialization
        self.root.geometry("800x400")
        
        #Creating the frame
        self.frame=ttk.Frame(self.root)
        
        #Creating a style object
        style = ttk.Style()
        
        #Configuring and applying frame style
        style.configure("Custom.TFrame", background="cadetblue")
        self.frame = ttk.Frame(self.root, style="Custom.TFrame")
        
        #Packing the frame to the window
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        #Adding the heading and packing it to the frame
        heading = tk.Label(self.frame, text="Personal Finance Tracker", font=("Forte", 27, "bold"),background="cadetblue")
        heading.pack(pady=(20,0))
        
        #Adding and packing a vertical scroll bar at the right of the frame
        scrollbar = tk.Scrollbar(self.frame, orient="vertical",width=15)
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y, padx=(0, 5), pady=(65,55))
        

        
        #Search bar and button
        #Creating a frame to place search entry bar and search button and packing it in the top center of the window
        search_container = tk.Frame(self.frame, background="cadetblue")
        search_container.pack(side=tk.TOP, anchor=tk.CENTER, pady=20)
        
        #Creating StringVar to store search query
        self.search = tk.StringVar()
        
        #Creating an entry widget for the search query and packing it
        search_entry = tk.Entry(search_container,text=self.search, width=20, font=("Times New Roman", 15))
        search_entry.pack(side=tk.LEFT)
        
        #Creating the search button and enabling search function to it 
        s_button = tk.Button(search_container, text="Search Transaction🔍 ", font=("Times New Roman", 10, "bold"), command=self.search_transactions, width=18)
        s_button.pack(side=tk.LEFT, padx=7)

        
    
        # Treeview for displaying transactions
        #Creating treeview widget with necessary columns 
        self.tree = ttk.Treeview(self.frame, columns=("Category", "Amount", "Type", "Date"), show="headings",yscrollcommand=scrollbar.set)
        
        #Configuring the style of the treeview and the style of the heading
        style.configure("Treeview", font=("Times New Roman", 12),background="White")
        style.configure("Treeview.Heading", font=("Times New Roman", 14, "bold"))
        
        #Defining the column names of the treeview            
        self.tree.heading("Category", text="Category", command=lambda: self.sort_by_column("Category", False), anchor="center")
        self.tree.heading("Amount", text="Amount", command=lambda: self.sort_by_column("Amount", False), anchor="center")
        self.tree.heading("Type", text="Type", command=lambda: self.sort_by_column("Type", False), anchor="center")
        self.tree.heading("Date", text="Date", command=lambda: self.sort_by_column("Date", False), anchor="center")

        #Setting column widths and alignment
        self.tree.column("Category", width=100, anchor="center")
        self.tree.column("Amount", width=100, anchor="center")
        self.tree.column("Type", width=100, anchor="center")
        self.tree.column("Date", width=100, anchor="center")
        
        self.tree.pack(fill=tk.BOTH,expand=True, padx=10, pady=(0,50)) 
        
        # Configuring the scrollbar to scroll the treeview when scrolling
        scrollbar.config(command=self.tree.yview)


        
        

    def load_transactions(self, filename):
        """Method to Load transactions from the JSON file"""
        try:
            #Loading transactions form the JSON file "transactions.json"
            with open(filename, "r") as file:
                transactions = json.load(file)
            #Returning the loaded transactions
            return transactions
        except FileNotFoundError:
            #Returning and empty dictionary if file is missing
            return {}

    def display_transactions(self, transactions):
        """Method to display transactions in the tree table"""
        
        #Remove existing entries
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add transactions to the treeview
        
        #Getting the data such as category,date,amount,transaction type from the dictionary
        for category,transaction_data in transactions.items():
            for transaction in transaction_data:
                date = transaction.get("date")
                amount = transaction.get("amount")
                transaction_type = transaction.get("type")
                
                # Inserting the transaction data into the tree view
                self.tree.insert("", "end", values=(category, amount, transaction_type, date))

    def search_transactions(self):
        """Method to search transactions by any attribute of the transaction"""
        #Getting search query from user and making it to simple letters
        search = self.search.get().lower()
        if search:
            output = {}
            #Iterating over all the category and transactions belongs to it
            for category, transaction_data in self.transactions.items():
                for transaction in transaction_data:
                    #Checking whether the search query matches with the category 
                    if search in category.lower():
                        #If not matching with category initializing a list for category
                        if category not in output:
                            output[category] = []
                        #Add transaction to the category's list if it matches
                        output[category].append(transaction)
                    else:
                        # Checking whether the search query matches any value in the transaction
                        for value in transaction.values():
                            if search in str(value).lower():
                                if category not in output:
                                    output[category] = []
                                output[category].append(transaction)
                                
                                #Breaking the loop after finding a match to avoid duplicates
                                break
            #Displaying the search results in the tree view
            self.display_transactions(output)
        else:
            #Displaying all the transactions if search query is empty
            self.display_transactions(self.transactions)

    


    def sort_by_column(self, col, reverse):
        """Method to sort columns in ascending or descending order"""

        if col == "Category":
            #Sorting the categories in alphabetical order
            categories = sorted(self.transactions.keys(), reverse=reverse)
            
            #Getting the current position of each category in the tree
            children = {child: self.tree.set(child, "Category") for child in self.tree.get_children()}
            index = 0
            
            #Moving each category to their sorted position through iteration
            for category in categories:
                #Iterating across each child item and its respective category values in the treeview
                for child, cat_value in children.items():
                    #Checking whether the category value of the child matches the current category in process
                    if cat_value == category:
                        #If yes, moving category to the new position 
                        self.tree.move(child, "", index)
                        #Increasing the index to reflect the new position for next upcoming category
                        index += 1
                        
        elif col == "Amount": 
            #Creating a list of tuples where each tuple contains the amount value of a transaction and its corresponding child item in the treeview  to sort amount
            value= [(float(self.tree.set(child, col)), child) for child in self.tree.get_children("")]
            value.sort(reverse=reverse)
            index = 0
            
            #Moving each transaction to its sorted position
            for data, child in value:
                self.tree.move(child, "", index)
                index += 1
        else:
            #Sorting for transaction type and transaction date
            value=[(self.tree.set(child, col), child) for child in self.tree.get_children("")]
            value.sort(reverse=reverse)
            index = 0
            for data, child in value:
                self.tree.move(child, "", index)
                index += 1
        #Set sorting indicator for the sorted column
        if reverse:
            sorting_indicator = "↓"
        else:
            sorting_indicator = "↑"
        
        column_heading = f"{col} {sorting_indicator}"
        
        #Updating the column heading in the treeview to indicate the sorting direction
        self.tree.heading(col,text=column_heading)

        # Toggling the sorting direction for next click on column heading
        self.tree.heading(col, command=lambda: self.sort_by_column(col, not reverse))

        
def main():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    app.display_transactions(app.transactions)
    root.mainloop()

if __name__ == "__main__":
    main()
