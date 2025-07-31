import csv
import os
import sys

# --- Configuration ---
# All file paths and credentials are set here for easy access.
STOCK_FILE = 'stock.csv'
SUPPLIER_FILE = 'suppliers.csv'
DATA_FILE = 'data.csv'
CREDENTIALS = {"admin": "test"}

# --- Data Loading and Saving Functions ---

def load_csv_data(file_path):
    """
    A general function to load any CSV file into a list of dictionaries.
    It checks if the file exists before trying to read it.
    """
    if not os.path.exists(file_path):
        # If a file is missing, the program can't run.
        print(f"\nCRITICAL ERROR: The data file '{file_path}' was not found.")
        print("Please make sure the required CSV files are in the same directory as the script.")
        sys.exit(1)
    
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            # The csv.DictReader automatically uses the first row as headers.
            return list(csv.DictReader(file))
    except Exception as e:
        print(f"\nCRITICAL ERROR: Could not read the file '{file_path}'. Reason: {e}")
        sys.exit(1)

def save_csv_data(file_path, data, headers):
    """
    A general function to save a list of dictionaries back to a CSV file.
    """
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"\nData successfully saved to {file_path}")
    except Exception as e:
        print(f"\nERROR: Could not save data to '{file_path}'. Reason: {e}")

# --- Core Logic Functions ---

def login():
    """
    Handles the user login process. Gives the user 3 attempts.
    """
    print("********** Welcome to the Cafe Management System **********")
    for attempt in range(3):
        username = input("Please enter your username: ").lower()
        if username in CREDENTIALS:
            password = input(f"Please enter the password for '{username}': ")
            if password == CREDENTIALS[username]:
                print("\nLogin successful! Welcome.")
                return True
            else:
                print("Incorrect password.")
        else:
            print("Username not found.")
    print("\nToo many failed login attempts. Exiting.")
    return False

def search_item(data, name):
    """
    Searches for an item in a list of dictionaries by its 'Name' field.
    The search is case-insensitive.
    """
    for item in data:
        if item['Name'].lower() == name.lower():
            return item
    return None

# --- Menu Functions ---

def product_menu(products):
    """
    Displays all products in the inventory.
    """
    print("\n--- All Products in Inventory ---")
    if not products:
        print("No products found.")
        return
        
    for p in products:
        try:
            # Ensures price and quantity are displayed correctly, even if data is messy.
            price = float(p.get('Price', 0))
            quantity = int(p.get('Quantity', 0))
            print(f"- {p.get('Name', 'N/A')} | Price: £{price:.2f} | Quantity: {quantity}")
        except (ValueError, TypeError):
            # This handles cases where Price or Quantity are not valid numbers.
            print(f"- {p.get('Name', 'N/A')} | Invalid data for this item.")
    input("\nPress Enter to return to the main menu.")

def supplier_menu(suppliers):
    """
    Displays all suppliers.
    """
    print("\n--- All Suppliers ---")
    if not suppliers:
        print("No suppliers found.")
        return

    for s in suppliers:
        print(f"- {s.get('Name', 'N/A')} | Category: {s.get('Supplier_Product_Category', 'N/A')} | Contact: {s.get('Supplier_Contact_Information', 'N/A')}")
    input("\nPress Enter to return to the main menu.")

def stock_menu(products):
    """
    Handles daily stock operations like sales and deliveries.
    """
    while True:
        print("\n--- Daily Stock Operations ---")
        print("1. Record a Sale")
        print("2. Receive a Delivery")
        print("3. View Stock Report")
        print("4. Return to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter the name of the product sold: ")
            product = search_item(products, name)
            if product:
                try:
                    current_stock = int(product.get('Quantity', 0))
                    quantity_sold = int(input(f"Enter quantity sold (Current stock: {current_stock}): "))
                    if 0 < quantity_sold <= current_stock:
                        product['Quantity'] = str(current_stock - quantity_sold)
                        save_csv_data(STOCK_FILE, products, ['Name', 'Price', 'Quantity'])
                    else:
                        print("Invalid quantity or not enough stock.")
                except (ValueError, TypeError):
                    print("Invalid input. Please enter a number for the quantity.")
            else:
                print("Product not found.")

        elif choice == '2':
            name = input("Enter the name of the product received: ")
            product = search_item(products, name)
            if product:
                try:
                    current_stock = int(product.get('Quantity', 0))
                    quantity_received = int(input("Enter quantity received: "))
                    if quantity_received > 0:
                        product['Quantity'] = str(current_stock + quantity_received)
                        save_csv_data(STOCK_FILE, products, ['Name', 'Price', 'Quantity'])
                    else:
                        print("Quantity must be a positive number.")
                except (ValueError, TypeError):
                    print("Invalid input. Please enter a number for the quantity.")
            else:
                print("Product not found.")

        elif choice == '3':
            print("\n--- Current Stock Report ---")
            for p in products:
                print(f"- {p.get('Name', 'N/A')}: {p.get('Quantity', 'N/A')} units")
        
        elif choice == '4':
            break # Exit the stock menu loop
        
        else:
            print("Invalid choice. Please try again.")

# --- Main Application ---

def main():
    """
    The main function that runs the entire application.
    """
    if not login():
        return # Exit if login fails

    # Load the data once at the start.
    products = load_csv_data(STOCK_FILE)
    suppliers = load_csv_data(SUPPLIER_FILE)

    while True:
        print("\n********** Main Menu **********")
        print("1. Product Management")
        print("2. Supplier Management")
        print("3. Daily Stock Operations")
        print("4. Exit System")
        print("*****************************")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            product_menu(products)
        elif choice == '2':
            supplier_menu(suppliers)
        elif choice == '3':
            stock_menu(products)
        elif choice == '4':
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# This is the entry point of the script.
if __name__ == '__main__':
    main()
