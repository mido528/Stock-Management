import csv
import os
import datetime
import sys
from enum import Enum
from abc import ABC, abstractmethod

# ==============================================================================
# DESIGN PATTERN: Singleton
# Manages global configuration settings like file paths and credentials.
# Ensures that there is only one instance of the configuration object.
# ==============================================================================
class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            # Initialize configuration values here
            cls._instance.stock_file = 'stock.csv'
            cls._instance.supplier_file = 'suppliers.csv'
            cls._instance.credentials = {"admin": "test"}
        return cls._instance

    def get_stock_file_path(self):
        return self.stock_file

    def get_supplier_file_path(self):
        return self.supplier_file

    def get_credentials(self):
        return self.credentials

# ==============================================================================
# DATA CLASSES: Define the core objects of our system.
# ==============================================================================
class Product:
    """A simple data class for a product."""
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price:.2f}, quantity={self.quantity})"

class Supplier:
    """A simple data class for a supplier."""
    def __init__(self, name, contact, category):
        self.name = name
        self.contact = contact
        self.category = category

    def __repr__(self):
        return f"Supplier(name='{self.name}', contact='{self.contact}', category='{self.category}')"

# ==============================================================================
# DESIGN PATTERN: Builder
# Provides a clean, step-by-step API for creating complex objects.
# ==============================================================================
class ProductBuilder:
    """Implements the Builder pattern for creating Product objects."""
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
        """Constructs and returns the final Product object."""
        if not self._name:
            raise ValueError("Product name must be set before building.")
        return Product(self._name, self._price, self._quantity)

# ==============================================================================
# DESIGN PATTERN: Inheritance (Abstract Base Class)
# Defines a common interface for all CSV-based manager classes.
# ==============================================================================
class CSVManager(ABC):
    """Abstract base class for managing data stored in a CSV file."""
    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error: The data file '{file_path}' was not found.")
        self.file_path = file_path
        self.items = self._load()

    def _load(self):
        items = []
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                items.append(self._row_to_object(row))
        return items

    def _save(self):
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            header = self._get_header()
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for item in self.items:
                writer.writerow(self._object_to_dict(item))
        print(f"Data successfully saved to {self.file_path}")

    @abstractmethod
    def _row_to_object(self, row):
        pass

    @abstractmethod
    def _object_to_dict(self, obj):
        pass

    @abstractmethod
    def _get_header(self):
        pass

# ==============================================================================
# Concrete Manager Classes (Inherit from CSVManager)
# ==============================================================================
class ProductManager(CSVManager):
    """Manages all product-related operations."""
    def _row_to_object(self, row):
        return Product(name=row['Name'], price=row['Price'], quantity=row['Quantity'])

    def _object_to_dict(self, product):
        return {'Name': product.name, 'Price': product.price, 'Quantity': product.quantity}

    def _get_header(self):
        return ['Name', 'Price', 'Quantity']

    def search_item(self, name):
        for product in self.items:
            if product.name.lower() == name.lower():
                return product
        return None

    def add_item(self, product):
        if self.search_item(product.name):
            print(f"Error: Product '{product.name}' already exists.")
            return
        self.items.append(product)
        self._save()

    def update_item(self, name, updated_product_data):
        product = self.search_item(name)
        if product:
            product.name = updated_product_data.name
            product.price = updated_product_data.price
            product.quantity = updated_product_data.quantity
            self._save()
            print(f"Product '{name}' updated successfully.")
        else:
            print(f"Error: Product '{name}' not found.")

    def delete_item(self, name):
        product = self.search_item(name)
        if product:
            self.items.remove(product)
            self._save()
            print(f"Product '{name}' deleted successfully.")
        else:
            print(f"Error: Product '{name}' not found.")

class SupplierManager(CSVManager):
    """Manages all supplier-related operations."""
    def _row_to_object(self, row):
        # This fixes the KeyError by using the correct header from your file
        return Supplier(name=row['Name'], contact=row['Supplier_Contact_Information'], category=row['Supplier_Product_Category'])

    def _object_to_dict(self, supplier):
        return {'Name': supplier.name, 'Supplier_Contact_Information': supplier.contact, 'Supplier_Product_Category': supplier.category}

    def _get_header(self):
        return ['Name', 'Supplier_Contact_Information', 'Supplier_Product_Category']

    def search_item(self, name):
        for supplier in self.items:
            if supplier.name.lower() == name.lower():
                return supplier
        return None

# ==============================================================================
# DESIGN PATTERN: Factory
# Centralizes the creation of manager objects.
# ==============================================================================
class ManagerFactory:
    """A factory for creating manager instances."""
    @staticmethod
    def create_manager(manager_type):
        config = Config()
        if manager_type == 'product':
            return ProductManager(config.get_stock_file_path())
        elif manager_type == 'supplier':
            return SupplierManager(config.get_supplier_file_path())
        raise ValueError(f"Unknown manager type: {manager_type}")

# ==============================================================================
# DESIGN PATTERN: Enum
# Provides readable, constant names for menu choices.
# ==============================================================================
class MenuChoice(Enum):
    PRODUCT_MANAGEMENT = '1'
    SUPPLIER_MANAGEMENT = '2'
    STOCK_MANAGEMENT = '3'
    EXIT = '4'

# ==============================================================================
# Main Application Class
# ==============================================================================
class CafeManagementApp:
    def __init__(self):
        self.config = Config()
        self.product_manager = ManagerFactory.create_manager('product')
        self.supplier_manager = ManagerFactory.create_manager('supplier')
        self.is_running = False

    def _login(self):
        """Handles the user login process."""
        print("********** Cafe Stock Management System **********")
        credentials = self.config.get_credentials()
        while True:
            username = input("Please enter your username: ").lower()
            if username in credentials:
                password = input(f"Please enter the password for '{username}': ")
                if password == credentials[username]:
                    print(f"\nLogin successful at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    return True
                else:
                    print("Incorrect password.")
            else:
                print("Username not found.")
            if input("Try again? (y/n): ").lower() != 'y':
                return False

    def run(self):
        """Main application loop."""
        if not self._login():
            print("Exiting application.")
            return

        self.is_running = True
        while self.is_running:
            self._display_main_menu()
            choice = input("Enter your choice: ")
            self._process_main_menu(choice)

    def _display_main_menu(self):
        print("\n********** Main Menu **********")
        print(f"{MenuChoice.PRODUCT_MANAGEMENT.value}. Product Management")
        print(f"{MenuChoice.SUPPLIER_MANAGEMENT.value}. Supplier Management")
        print(f"{MenuChoice.STOCK_MANAGEMENT.value}. Daily Stock Operations")
        print(f"{MenuChoice.EXIT.value}. Exit System")
        print("*****************************")

    def _process_main_menu(self, choice):
        if choice == MenuChoice.PRODUCT_MANAGEMENT.value:
            self._product_menu()
        elif choice == MenuChoice.SUPPLIER_MANAGEMENT.value:
            print("\nSupplier management is a planned feature.") # Placeholder
        elif choice == MenuChoice.STOCK_MANAGEMENT.value:
            self._stock_menu()
        elif choice == MenuChoice.EXIT.value:
            self.is_running = False
            print("Exiting the Cafe Management System. Goodbye!")
        else:
            print("Invalid choice. Please try again.")

    def _product_menu(self):
        """Displays and handles the product management sub-menu."""
        while True:
            print("\n--- Product Management ---")
            print("1. Add New Product")
            print("2. Update Product")
            print("3. Delete Product")
            print("4. View All Products")
            print("5. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                try:
                    # Using the builder for clean object creation
                    builder = ProductBuilder()
                    name = input("Enter product name: ")
                    price = input("Enter product price: ")
                    quantity = input("Enter initial quantity: ")
                    new_product = builder.with_name(name).with_price(price).with_quantity(quantity).build()
                    self.product_manager.add_item(new_product)
                except (ValueError, TypeError) as e:
                    print(f"Error creating product: {e}")
            elif choice == '4':
                print("\n--- All Products ---")
                for p in self.product_manager.items:
                    print(f"- {p.name} | Price: £{p.price:.2f} | Quantity: {p.quantity}")
            elif choice == '5':
                break
            else:
                print("Invalid choice or feature not yet implemented.")


    def _stock_menu(self):
        """Displays and handles the daily stock operations sub-menu."""
        while True:
            print("\n--- Daily Stock Operations ---")
            print("1. Record Sales")
            print("2. Receive Stock Delivery")
            print("3. View Stock Report")
            print("4. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                name = input("Enter product name sold: ")
                product = self.product_manager.search_item(name)
                if product:
                    try:
                        quantity = int(input(f"Enter quantity sold (Current stock: {product.quantity}): "))
                        if 0 < quantity <= product.quantity:
                            product.quantity -= quantity
                            self.product_manager._save()
                            print(f"Sale recorded. New quantity for '{name}': {product.quantity}")
                        else:
                            print("Invalid quantity or not enough stock.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                else:
                    print("Product not found.")
            elif choice == '3':
                self._stock_report()
            elif choice == '4':
                break
            else:
                print("Invalid choice or feature not yet implemented.")

    def _stock_report(self):
        print("\n--- Stock Report ---")
        for p in self.product_manager.items:
            print(f"- {p.name}: {p.quantity}")


if __name__ == '__main__':
    try:
        app = CafeManagementApp()
        app.run()
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
