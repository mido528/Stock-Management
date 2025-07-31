import csv
import os
import datetime
import sys
from enum import Enum
from abc import ABC, abstractmethod

# ==============================================================================
# DESIGN PATTERN: Singleton
# This class holds all our application's settings. By making it a Singleton,
# we ensure that there's only one instance of these settings, providing a
# single, reliable source of truth for file paths and credentials.
# ==============================================================================
class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.stock_file = 'stock.csv'
            cls._instance.supplier_file = 'suppliers.csv'
            cls._instance.credentials = {"admin": "test"}
        return cls._instance

# ==============================================================================
# DATA CLASSES: Simple containers for our data.
# Using classes instead of dictionaries makes the code clearer and safer.
# ==============================================================================
class Product:
    """Represents a single product with its name, price, and quantity."""
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)

    def __repr__(self):
        """A developer-friendly string representation of the Product object."""
        return f"Product(name='{self.name}', price={self.price:.2f}, quantity={self.quantity})"

class Supplier:
    """Represents a single supplier."""
    def __init__(self, name, contact, category):
        self.name = name
        self.contact = contact
        self.category = category

    def __repr__(self):
        return f"Supplier(name='{self.name}', contact='{self.contact}', category='{self.category}')"

# ==============================================================================
# DESIGN PATTERN: Builder
# This pattern provides a clean, step-by-step way to create objects.
# It's much more readable than creating a dictionary or passing many arguments.
# ==============================================================================
class ProductBuilder:
    """A builder for creating Product objects in a fluent, step-by-step way."""
    def __init__(self):
        self._name = None
        self._price = 0.0
        self._quantity = 0

    def with_name(self, name):
        self._name = name
        return self

    def with_price(self, price):
        self._price = float(price)
        return self

    def with_quantity(self, quantity):
        self._quantity = int(quantity)
        return self

    def build(self):
        """Creates the final Product object from the provided details."""
        if not self._name:
            raise ValueError("Product name is required.")
        return Product(self._name, self._price, self._quantity)

# ==============================================================================
# DESIGN PATTERN: Inheritance (using an Abstract Base Class)
# This base class handles all the boring file work (reading/writing CSVs).
# Other "manager" classes can inherit from it to avoid repeating code.
# ==============================================================================
class CSVManager(ABC):
    """An abstract base class for any class that needs to manage a CSV file."""
    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error: The data file '{file_path}' was not found.")
        self.file_path = file_path
        self.items = self._load()

    def _load(self):
        """Loads all rows from the CSV file."""
        items = []
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                items.append(self._row_to_object(row))
        return items

    def _save(self):
        """Saves all current items back to the CSV file."""
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            header = self._get_header()
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for item in self.items:
                writer.writerow(self._object_to_dict(item))
        print(f"\nData successfully saved to {self.file_path}")

    @abstractmethod
    def _row_to_object(self, row):
        """Subclasses must implement this to turn a CSV row into an object."""
        pass

    @abstractmethod
    def _object_to_dict(self, obj):
        """Subclasses must implement this to turn an object into a dictionary for saving."""
        pass

    @abstractmethod
    def _get_header(self):
        """Subclasses must provide the CSV header."""
        pass

# ==============================================================================
# Concrete Manager Classes that inherit from CSVManager
# ==============================================================================
class ProductManager(CSVManager):
    """Manages all operations for products, inheriting file logic from CSVManager."""
    def _row_to_object(self, row):
        return Product(name=row['Name'], price=row['Price'], quantity=row['Quantity'])

    def _object_to_dict(self, product):
        return {'Name': product.name, 'Price': product.price, 'Quantity': product.quantity}

    def _get_header(self):
        return ['Name', 'Price', 'Quantity']

    def search_item(self, name):
        """Finds a product by its name (case-insensitive)."""
        for product in self.items:
            if product.name.lower() == name.lower():
                return product
        return None

class SupplierManager(CSVManager):
    """Manages all operations for suppliers."""
    def _row_to_object(self, row):
        # This fixes the original KeyError by using the correct headers.
        return Supplier(name=row['Name'], contact=row['Supplier_Contact_Information'], category=row['Supplier_Product_Category'])

    def _object_to_dict(self, supplier):
        return {'Name': supplier.name, 'Supplier_Contact_Information': supplier.contact, 'Supplier_Product_Category': supplier.category}

    def _get_header(self):
        return ['Name', 'Supplier_Contact_Information', 'Supplier_Product_Category']

# ==============================================================================
# DESIGN PATTERN: Factory
# This class is a central place for creating our manager objects.
# It makes the main application cleaner and easier to change later.
# ==============================================================================
class ManagerFactory:
    """A factory for creating different types of manager classes."""
    @staticmethod
    def create(manager_type):
        config = Config()
        if manager_type == 'product':
            return ProductManager(config.stock_file)
        elif manager_type == 'supplier':
            return SupplierManager(config.supplier_file)
        raise ValueError(f"Unknown manager type: {manager_type}")

# ==============================================================================
# DESIGN PATTERN: Enum
# This makes our menu choices more readable and less prone to typos
# than using simple strings or numbers.
# ==============================================================================
class Menu(Enum):
    PRODUCTS = '1'
    SUPPLIERS = '2'
    STOCK = '3'
    EXIT = '4'

# ==============================================================================
# The Main Application Class
# This class brings everything together to run the application.
# ==============================================================================
class CafeApp:
    def __init__(self):
        """Initializes the application by creating the necessary managers."""
        self.config = Config()
        self.product_manager = ManagerFactory.create('product')
        self.supplier_manager = ManagerFactory.create('supplier')
        self.is_running = False

    def start(self):
        """The main entry point to run the application."""
        if not self._login():
            print("Exiting application.")
            return

        self.is_running = True
        while self.is_running:
            self._display_main_menu()
            choice = input("Enter your choice: ")
            self._handle_main_menu_choice(choice)

    def _login(self):
        """Handles the user login screen."""
        print("********** Welcome to the Cafe Management System **********")
        credentials = self.config.credentials
        for _ in range(3):  # Give user 3 attempts
            username = input("Please enter your username: ").lower()
            if username in credentials:
                password = input(f"Please enter the password for '{username}': ")
                if password == credentials[username]:
                    print(f"\nLogin successful! Welcome.")
                    return True
                else:
                    print("Incorrect password.")
            else:
                print("Username not found.")
        print("Too many failed login attempts.")
        return False

    def _display_main_menu(self):
        """Shows the main menu options to the user."""
        print("\n********** Main Menu **********")
        print(f"{Menu.PRODUCTS.value}. Product Management")
        print(f"{Menu.SUPPLIERS.value}. Supplier Management")
        print(f"{Menu.STOCK.value}. Daily Stock Operations")
        print(f"{Menu.EXIT.value}. Exit System")
        print("*****************************")

    def _handle_main_menu_choice(self, choice):
        """Directs the user to the correct sub-menu based on their choice."""
        if choice == Menu.PRODUCTS.value:
            self._product_menu()
        elif choice == Menu.SUPPLIERS.value:
            self._supplier_menu()
        elif choice == Menu.STOCK.value:
            self._stock_menu()
        elif choice == Menu.EXIT.value:
            self.is_running = False
            print("Thank you for using the system. Goodbye!")
        else:
            print("Invalid choice. Please try again.")

    def _product_menu(self):
        """Handles all logic for the Product Management sub-menu."""
        print("\n--- Product Management ---")
        # This menu is a placeholder for now, you can add more options here.
        print("\n--- All Products ---")
        for p in self.product_manager.items:
            print(f"- {p.name} | Price: £{p.price:.2f} | Quantity: {p.quantity}")
        input("\nPress Enter to return to the main menu.")

    def _supplier_menu(self):
        """Handles all logic for the Supplier Management sub-menu."""
        print("\n--- Supplier Management ---")
        print("\n--- All Suppliers ---")
        for s in self.supplier_manager.items:
            print(f"- {s.name} | Category: {s.category} | Contact: {s.contact}")
        input("\nPress Enter to return to the main menu.")


    def _stock_menu(self):
        """Handles daily stock tasks like sales and deliveries."""
        print("\n--- Daily Stock Operations ---")
        print("1. Record a Sale")
        print("2. Receive a Delivery")
        print("3. View Stock Report")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter the name of the product sold: ")
            product = self.product_manager.search_item(name)
            if product:
                try:
                    quantity = int(input(f"Enter quantity sold (Current stock: {product.quantity}): "))
                    if 0 < quantity <= product.quantity:
                        product.quantity -= quantity
                        self.product_manager._save()
                    else:
                        print("Invalid quantity or not enough stock.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            else:
                print("Product not found.")
        elif choice == '2':
            name = input("Enter the name of the product received: ")
            product = self.product_manager.search_item(name)
            if product:
                try:
                    quantity = int(input("Enter quantity received: "))
                    if quantity > 0:
                        product.quantity += quantity
                        self.product_manager._save()
                    else:
                        print("Quantity must be positive.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            else:
                print("Product not found.")
        elif choice == '3':
            self._stock_report()
        else:
            print("Invalid choice.")
        input("\nPress Enter to return to the main menu.")


    def _stock_report(self):
        """Prints a simple report of current stock levels."""
        print("\n--- Current Stock Report ---")
        for p in self.product_manager.items:
            print(f"- {p.name}: {p.quantity} units")


if __name__ == '__main__':
    try:
        # This is the entry point of our application.
        app = CafeApp()
        app.start()
    except FileNotFoundError as e:
        print(f"\nCRITICAL ERROR: {e}")
        print("Please make sure 'stock.csv' and 'suppliers.csv' are in the same directory.")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)
