import csv
import os
import datetime
import sys

# --- Class Definitions ---
# I have recreated the necessary classes that were previously in separate modules.

class Utils:
    """A utility class for helper functions like getting the current time."""
    def format_date(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class ProductManager:
    """Handles all operations related to products in a CSV file."""
    def __init__(self, file_path):
        self.file_path = file_path
        self.products = self._load()

    def _load(self):
        products = []
        if os.path.exists(self.file_path):
            with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    products.append({
                        'name': row['Name'],
                        'price': float(row['Price']),
                        'quantity': int(row['Quantity'])
                    })
        return products

    def _save(self):
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['Name', 'Price', 'Quantity']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for product in self.products:
                writer.writerow({
                    'Name': product['name'],
                    'Price': product['price'],
                    'Quantity': product['quantity']
                })
        print(f"Product data saved to {self.file_path}")

    def get_all_products(self):
        return self.products

    def search_product(self, product_name):
        for product in self.products:
            if product['name'].lower() == product_name.lower():
                return product
        return None

    def add_product(self, product):
        if self.search_product(product['name']):
            print(f"Error: Product '{product['name']}' already exists.")
            return
        self.products.append(product)
        self._save()
        print(f"Product '{product['name']}' added successfully.")

    def update_product(self, product_name, updated_product):
        for i, product in enumerate(self.products):
            if product['name'].lower() == product_name.lower():
                self.products[i] = updated_product
                self._save()
                return True
        return False

    def delete_product(self, product_name):
        product_to_delete = self.search_product(product_name)
        if product_to_delete:
            self.products.remove(product_to_delete)
            self._save()
            return True
        return False

class SupplierManager:
    """Handles all operations related to suppliers in a CSV file."""
    def __init__(self, file_path):
        self.file_path = file_path
        self.suppliers = self._load()

    def _load(self):
        suppliers = []
        if os.path.exists(self.file_path):
            with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    suppliers.append({
                        'name': row['Name'],
                        'contact': row['ContactInfo'],
                        'category': row['ProductCategory']
                    })
        return suppliers

    def _save(self):
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['Name', 'ContactInfo', 'ProductCategory']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for supplier in self.suppliers:
                writer.writerow({
                    'Name': supplier['name'],
                    'ContactInfo': supplier['contact'],
                    'ProductCategory': supplier['category']
                })
        print(f"Supplier data saved to {self.file_path}")

    def get_all_suppliers(self):
        return self.suppliers

    def search_supplier(self, supplier_name):
        for supplier in self.suppliers:
            if supplier['name'].lower() == supplier_name.lower():
                return supplier
        return None

    def add_supplier(self, supplier):
        if self.search_supplier(supplier['name']):
            print(f"Error: Supplier '{supplier['name']}' already exists.")
            return
        self.suppliers.append(supplier)
        self._save()
        print(f"Supplier '{supplier['name']}' added successfully.")

    def update_supplier(self, supplier_name, updated_supplier):
        for i, supplier in enumerate(self.suppliers):
            if supplier['name'].lower() == supplier_name.lower():
                self.suppliers[i] = updated_supplier
                self._save()
                return True
        return False

    def delete_supplier(self, supplier_name):
        supplier_to_delete = self.search_supplier(supplier_name)
        if supplier_to_delete:
            self.suppliers.remove(supplier_to_delete)
            self._save()
            return True
        return False

class PurchaseOrder:
    """A simple class to represent a purchase order."""
    def __init__(self, product_name, quantity):
        self.product_name = product_name
        self.quantity = quantity
        self.date = datetime.date.today().isoformat()

    def generate_order(self):
        # In a real system, this would save to a PO file or database.
        # For this example, we just print a confirmation.
        print(f"--- Purchase Order Generated ---")
        print(f"Date: {self.date}")
        print(f"Product: {self.product_name}")
        print(f"Quantity: {self.quantity}")
        print("--------------------------------")


# --- Main Application Logic ---

def login_system():
    """Handles the user login process."""
    admin_credentials = {"admin": "test"}
    print("********** Cafe Stock Management System **********")
    print("********** Login System **********")
    while True:
        username = input("Please enter your username: ").lower()
        if username in admin_credentials:
            password = input(f"Please enter the password for the '{username}' account: ")
            if password == admin_credentials[username]:
                time = Utils()
                print(f"\nLogin successful\nTime: {time.format_date()}")
                return True
            else:
                print("Incorrect password. Please try again.")
        else:
            print("Username not found. Please try again.")

def product_manager_system(product_manager):
    """Menu system for managing products."""
    while True:
        print("\n=== Cafe Product Management ===")
        print("1. Add new cafe product")
        print("2. Update product details")
        print("3. Remove product from inventory")
        print("4. Search product information")
        print("5. View all products")
        print("6. Return to main menu")
        choice = input("\nEnter your choice: ")

        if choice == '1':
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter initial stock quantity: "))
            product_manager.add_product({'name': name, 'price': price, 'quantity': quantity})
        elif choice == '2':
            name = input("Enter product name to update: ")
            product = product_manager.search_product(name)
            if not product:
                print("Product not found!")
                continue
            new_name = input(f"Enter new name (current: {product['name']}) or leave blank: ") or product['name']
            new_price = input(f"Enter new price (current: {product['price']}) or leave blank: ") or product['price']
            new_quantity = input(f"Enter new quantity (current: {product['quantity']}) or leave blank: ") or product['quantity']
            updated_product = {'name': new_name, 'price': float(new_price), 'quantity': int(new_quantity)}
            product_manager.update_product(name, updated_product)
        elif choice == '3':
            name = input("Enter product name to remove: ")
            if product_manager.delete_product(name):
                print(f"'{name}' removed successfully.")
            else:
                print(f"Could not find '{name}' to remove.")
        elif choice == '4':
            name = input("Enter product name to search: ")
            product = product_manager.search_product(name)
            if product:
                print(f"\nDetails: Name: {product['name']}, Price: £{product['price']:.2f}, Quantity: {product['quantity']}")
            else:
                print("Product not found.")
        elif choice == '5':
            for p in product_manager.get_all_products():
                print(f"- {p['name']} | Price: £{p['price']:.2f} | Quantity: {p['quantity']}")
        elif choice == '6':
            break
        else:
            print("Invalid choice.")

def supplier_manager_system(supplier_manager):
    """Menu system for managing suppliers."""
    while True:
        print("\n=== Cafe Supplier Management ===")
        print("1. Add new supplier")
        print("2. Update supplier details")
        print("3. Remove supplier")
        print("4. Search for a supplier")
        print("5. View all suppliers")
        print("6. Return to main menu")
        choice = input("\nEnter your choice: ")

        if choice == '1':
            name = input("Enter supplier name: ")
            contact = input("Enter contact info: ")
            category = input("Enter product category: ")
            supplier_manager.add_supplier({'name': name, 'contact': contact, 'category': category})
        elif choice == '2':
            name = input("Enter supplier name to update: ")
            supplier = supplier_manager.search_supplier(name)
            if not supplier:
                print("Supplier not found!")
                continue
            new_name = input(f"Enter new name (current: {supplier['name']}) or leave blank: ") or supplier['name']
            new_contact = input(f"Enter new contact (current: {supplier['contact']}) or leave blank: ") or supplier['contact']
            new_category = input(f"Enter new category (current: {supplier['category']}) or leave blank: ") or supplier['category']
            updated_supplier = {'name': new_name, 'contact': new_contact, 'category': new_category}
            supplier_manager.update_supplier(name, updated_supplier)
        elif choice == '3':
            name = input("Enter supplier name to remove: ")
            if supplier_manager.delete_supplier(name):
                print(f"'{name}' removed successfully.")
            else:
                print(f"Could not find '{name}' to remove.")
        elif choice == '4':
            name = input("Enter supplier name to search: ")
            supplier = supplier_manager.search_supplier(name)
            if supplier:
                print(f"\nDetails: Name: {supplier['name']}, Contact: {supplier['contact']}, Category: {supplier['category']}")
            else:
                print("Supplier not found.")
        elif choice == '5':
            for s in supplier_manager.get_all_suppliers():
                print(f"- {s['name']} | Category: {s['category']} | Contact: {s['contact']}")
        elif choice == '6':
            break
        else:
            print("Invalid choice.")

def stock_management_system(product_manager):
    """Menu system for daily stock operations."""
    stock_manager = product_manager # Use the same product manager instance
    while True:
        print("\n=== Daily Stock Management ===")
        print("1. Receive stock delivery")
        print("2. Record sales")
        print("3. View stock report")
        print("4. Return to main menu")
        choice = input("\nEnter your choice: ")

        if choice == '1':
            name = input("Enter product name received: ")
            product = stock_manager.search_product(name)
            if product:
                quantity = int(input(f"Enter quantity of '{name}' received: "))
                product['quantity'] += quantity
                stock_manager._save()
                print(f"Stock updated. New quantity for '{name}': {product['quantity']}")
            else:
                print("Product not found.")
        elif choice == '2':
            name = input("Enter product name sold: ")
            product = stock_manager.search_product(name)
            if product:
                quantity = int(input(f"Enter quantity of '{name}' sold: "))
                if product['quantity'] >= quantity:
                    product['quantity'] -= quantity
                    stock_manager._save()
                    print(f"Sale recorded. New quantity for '{name}': {product['quantity']}")
                else:
                    print(f"Error: Not enough stock. Only {product['quantity']} available.")
            else:
                print("Product not found.")
        elif choice == '3':
            print("\n--- Stock Report ---")
            for p in stock_manager.get_all_products():
                print(f"- {p['name']}: {p['quantity']}")
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

def purchase_order_system(product_manager):
    """Menu system for generating purchase orders."""
    while True:
        print("\n=== Cafe Purchase Orders ===")
        print("1. Generate order for low stock items")
        print("2. Create custom purchase order")
        print("3. Return to main menu")
        choice = input("\nEnter your choice: ")

        if choice == '1':
            threshold = int(input("Enter low stock threshold (e.g., 20): ") or 20)
            low_stock_items = [p for p in product_manager.get_all_products() if p['quantity'] < threshold]
            if not low_stock_items:
                print("No items are below the stock threshold.")
                continue
            print("\nItems below threshold:")
            for item in low_stock_items:
                print(f"- {item['name']} (Current: {item['quantity']})")
            if input("Generate orders for these items? (y/n): ").lower() == 'y':
                for item in low_stock_items:
                    order_qty = int(input(f"Enter order quantity for {item['name']}: "))
                    po = PurchaseOrder(item['name'], order_qty)
                    po.generate_order()
        elif choice == '2':
            name = input("Enter product name for custom order: ")
            if product_manager.search_product(name):
                quantity = int(input(f"Enter quantity to order for '{name}': "))
                po = PurchaseOrder(name, quantity)
                po.generate_order()
            else:
                print("Product not found.")
        elif choice == '3':
            break
        else:
            print("Invalid choice.")


def main():
    """Main function to run the application."""
    # Correctly point to the data files in the same directory
    stock_file = 'stock.csv'
    supplier_file = 'suppliers.csv'

    if not os.path.exists(stock_file) or not os.path.exists(supplier_file):
        print(f"Error: Make sure '{stock_file}' and '{supplier_file}' exist in the same directory as the script.")
        sys.exit(1)

    if not login_system():
        return

    # Instantiate managers once
    product_manager = ProductManager(stock_file)
    supplier_manager = SupplierManager(supplier_file)

    while True:
        print("\n********** Main Menu **********")
        print("1. Product Management")
        print("2. Supplier Management")
        print("3. Stock Management")
        print("4. Purchase Orders")
        print("5. Exit System")
        choice = input("\nEnter your choice: ")

        if choice == '1':
            product_manager_system(product_manager)
        elif choice == '2':
            supplier_manager_system(supplier_manager)
        elif choice == '3':
            stock_management_system(product_manager) # Stock uses the product data
        elif choice == '4':
            purchase_order_system(product_manager)
        elif choice == '5':
            print("Exiting the Cafe Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
