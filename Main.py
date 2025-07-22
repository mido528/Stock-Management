import os
import sys
from modules.product import Product
from modules.supplier import Supplier
from modules.utils import Utils
from modules.stock import Stock
from modules.purchase_order import PurchaseOrder

# Ensure the program can find the data files
DATA_FILE = os.path.join(os.path.dirname(__file__), 'datas', 'data.csv')
SUPPLIER_FILE = os.path.join(os.path.dirname(__file__), 'datas', 'supplier_data.csv')

# User login system
admin_username = ["admin", "ADMIN"]
admin_password = ["test", "TEST"]

time = Utils()
print("********** Cafe Stock Management System **********")
print("********** Login System **********")
while True:
    username_input = input("Please enter your username: ")
    if username_input.lower() in admin_username:
        password_input = input(f"Please enter the password for *{username_input}* account: ")
        if password_input.lower() in admin_password:
            print("\nLogin successful\nTime : " + time.format_date())
            break
        else:
            print(f"Incorrect password for {username_input}, try the login system again")
    else:
        print("Login error. Please try again")

# Product manager system
def product_manager_system():
    product_manager = Product('../datas/data.csv')  # Updated to use the cafe products CSV

    while True:
        print("\n=== Cafe Product Management ===")
        print("1. Add new cafe product")
        print("2. Update product details")
        print("3. Remove product from inventory")
        print("4. Search product information")
        print("5. View all products")
        print("6. Return to main menu")

        product_choice = input("\nEnter your choice: ")

        if product_choice == '1':
            print("\nAdding new cafe product:")
            product_name = input("Enter product name (e.g., 'Latte Mix'): ")
            product_price = float(input("Enter product price per unit (e.g., 3.50): "))
            product_quantity = int(input("Enter initial stock quantity: "))
            product = {'name': product_name, 'price': product_price, 'quantity': product_quantity}
            product_manager.add_product(product)
            product_manager.save_products()

        elif product_choice == '2':
            product_name = input("Enter product name to update: ")
            print(f"Updating {product_name}:")
            updated_product_name = input("Enter updated product name (leave blank to keep current): ")
            updated_product_price = input("Enter updated product price (leave blank to keep current): ")
            updated_product_quantity = input("Enter updated product quantity (leave blank to keep current): ")
            
            # Get current product details
            current_product = product_manager.search_product(product_name)
            if not current_product:
                print("Product not found!")
                continue
                
            updated_product = {
                'name': updated_product_name if updated_product_name else current_product['name'],
                'price': float(updated_product_price) if updated_product_price else current_product['price'],
                'quantity': int(updated_product_quantity) if updated_product_quantity else current_product['quantity']
            }
            product_manager.update_product(product_name, updated_product)
            product_manager.save_products()
            print(f"{product_name} updated successfully!")

        elif product_choice == '3':
            product_name = input("Enter product name to remove from inventory: ")
            confirm = input(f"Are you sure you want to remove {product_name}? (y/n): ")
            if confirm.lower() == 'y':
                product_manager.delete_product(product_name)
                product_manager.save_products()
                print(f"{product_name} removed from inventory.")

        elif product_choice == '4':
            product_name = input("Enter product name to search: ")
            product = product_manager.search_product(product_name)
            if product:
                print("\nProduct Details:")
                print(f"Name: {product['name']}")
                print(f"Price: £{product['price']:.2f}")
                print(f"Current Stock: {product['quantity']}")
            else:
                print("Product not found.")

        elif product_choice == '5':
            print("\nCurrent Cafe Inventory:")
            products = product_manager.get_all_products()
            for product in products:
                print(f"{product['name']} - £{product['price']:.2f} - Qty: {product['quantity']}")

        elif product_choice == '6':
            break

        else:
            print("Invalid choice. Please try again.")

# Supplier manager system
def supplier_manager_system():
    supplier_manager = Supplier('../datas/supplier_data.csv')  # Updated to use the cafe suppliers CSV

    while True:
        print("\n=== Cafe Supplier Management ===")
        print("1. Add new supplier")
        print("2. Update supplier details")
        print("3. Remove supplier")
        print("4. Search supplier information")
        print("5. View all suppliers")
        print("6. Return to main menu")

        supplier_choice = input("\nEnter your choice: ")

        if supplier_choice == '1':
            print("\nAdding new cafe supplier:")
            supplier_name = input("Enter supplier name: ")
            supplier_contact = input("Enter contact information (email/phone): ")
            supplier_category = input("Enter product category (e.g., 'Coffee Beans & Tea'): ")
            supplier = {
                'name': supplier_name, 
                'supplier_contact_information': supplier_contact,
                'supplier_product_category': supplier_category
            }
            supplier_manager.add_supplier(supplier)
            supplier_manager.save_supplier()

        elif supplier_choice == '2':
            supplier_name = input("Enter supplier name to update: ")
            current_supplier = supplier_manager.search_supplier(supplier_name)
            if not current_supplier:
                print("Supplier not found!")
                continue
                
            print(f"\nUpdating {supplier_name}:")
            updated_name = input(f"Enter updated name (current: {current_supplier['name']}): ")
            updated_contact = input(f"Enter updated contact (current: {current_supplier['supplier_contact_information']}): ")
            updated_category = input(f"Enter updated category (current: {current_supplier['supplier_product_category']}): ")
            
            updated_supplier = {
                'name': updated_name if updated_name else current_supplier['name'],
                'supplier_contact_information': updated_contact if updated_contact else current_supplier['supplier_contact_information'],
                'supplier_product_category': updated_category if updated_category else current_supplier['supplier_product_category']
            }
            supplier_manager.update_supplier(supplier_name, updated_supplier)
            supplier_manager.save_supplier()
            print("Supplier updated successfully!")

        elif supplier_choice == '3':
            supplier_name = input("Enter supplier name to remove: ")
            confirm = input(f"Are you sure you want to remove {supplier_name}? (y/n): ")
            if confirm.lower() == 'y':
                supplier_manager.delete_supplier(supplier_name)
                supplier_manager.save_supplier()
                print(f"{supplier_name} removed from suppliers.")

        elif supplier_choice == '4':
            supplier_name = input("Enter supplier name to search: ")
            supplier = supplier_manager.search_supplier(supplier_name)
            if supplier:
                print("\nSupplier Details:")
                print(f"Name: {supplier['name']}")
                print(f"Contact: {supplier['supplier_contact_information']}")
                print(f"Product Category: {supplier['supplier_product_category']}")
            else:
                print("Supplier not found.")

        elif supplier_choice == '5':
            print("\nCurrent Cafe Suppliers:")
            suppliers = supplier_manager.get_all_suppliers()
            for supplier in suppliers:
                print(f"{supplier['name']} - {supplier['supplier_product_category']} - Contact: {supplier['supplier_contact_information']}")

        elif supplier_choice == '6':
            break

        else:
            print("Invalid choice. Please try again.")

# Purchase order system for cafe
def purchase_order_system():
    product_manager = Product('../datas/data.csv')
    
    while True:
        print("\n=== Cafe Purchase Orders ===")
        print("1. Generate order for low stock items")
        print("2. Create custom purchase order")
        print("3. View current stock levels")
        print("4. Return to main menu")
        
        po_choice = input("\nEnter your choice: ")
        
        if po_choice == '1':
            # Automatic low stock detection
            threshold = int(input("Enter low stock threshold (default 10): ") or 10)
            low_stock_items = []
            
            products = product_manager.get_all_products()
            for product in products:
                if product['quantity'] < threshold:
                    low_stock_items.append(product)
            
            if not low_stock_items:
                print("No items below stock threshold!")
                continue
                
            print("\nLow Stock Items:")
            for item in low_stock_items:
                print(f"{item['name']} - Current: {item['quantity']}")
            
            confirm = input("\nGenerate purchase orders for these items? (y/n): ")
            if confirm.lower() == 'y':
                for item in low_stock_items:
                    quantity = int(input(f"Enter order quantity for {item['name']} (suggested {threshold*2 - item['quantity']}): "))
                    po = PurchaseOrder(item['name'], quantity)
                    po.generate_order()
                    print(f"Order generated for {item['name']}")
        
        elif po_choice == '2':
            # Manual order creation
            product_name = input("Enter the product name: ")
            product = product_manager.search_product(product_name)
            if not product:
                print("Product not found!")
                continue
                
            print(f"Current stock: {product['quantity']}")
            quantity = int(input("Enter the quantity to order: "))
            
            po = PurchaseOrder(product_name, quantity)
            po.generate_order()
            print(f"Purchase order generated for {quantity} units of {product_name}")
        
        elif po_choice == '3':
            print("\nCurrent Stock Levels:")
            products = product_manager.get_all_products()
            for product in products:
                print(f"{product['name']}: {product['quantity']} units")
        
        elif po_choice == '4':
            break
        
        else:
            print("Invalid choice. Please try again.")

# Stock management system for cafe
def stock_management_system():
    stock_manager = Stock('../datas/data.csv')
    
    while True:
        print("\n=== Cafe Stock Management ===")
        print("1. Receive new stock delivery")
        print("2. Record daily sales")
        print("3. View current stock report")
        print("4. Adjust stock levels (manual correction)")
        print("5. Return to main menu")

        stock_choice = input("\nEnter your choice: ")

        if stock_choice == '1':
            print("\nReceiving New Stock:")
            product_name = input("Enter product name: ")
            product = stock_manager.search_product(product_name)
            if not product:
                print("Product not found!")
                continue
                
            print(f"Current stock: {product['quantity']}")
            quantity = int(input("Enter quantity received: "))
            stock_manager.receive_stock(product_name, quantity)
            print(f"{quantity} units of {product_name} added to stock. New total: {product['quantity'] + quantity}")

        elif stock_choice == '2':
            print("\nRecording Sales:")
            product_name = input("Enter product name sold: ")
            product = stock_manager.search_product(product_name)
            if not product:
                print("Product not found!")
                continue
                
            print(f"Current stock: {product['quantity']}")
            quantity = int(input("Enter quantity sold: "))
            if quantity > product['quantity']:
                print("Warning: Not enough stock! Sale not recorded.")
                continue
                
            stock_manager.record_sale(product_name, quantity)
            print(f"Sale recorded. {quantity} units of {product_name} removed from stock.")

        elif stock_choice == '3':
            print("\nCurrent Stock Report:")
            stock_manager.generate_stock_report()

        elif stock_choice == '4':
            print("\nManual Stock Adjustment:")
            product_name = input("Enter product name: ")
            product = stock_manager.search_product(product_name)
            if not product:
                print("Product not found!")
                continue
                
            print(f"Current stock: {product['quantity']}")
            new_quantity = int(input("Enter new stock quantity: "))
            reason = input("Enter reason for adjustment (e.g., 'wastage', 'inventory correction'): ")
            stock_manager.adjust_stock(product_name, new_quantity, reason)
            print(f"Stock level for {product_name} updated to {new_quantity}")

        elif stock_choice == '5':
            break

        else:
            print("Invalid choice. Please try again.")

# Main menu for cafe management
if __name__ == '__main__':
    while True:
        print("\n********** Cafe Stock Management System **********")
        print("\n1. Product Management")
        print("2. Supplier Management")
        print("3. Purchase Orders")
        print("4. Stock Management")
        print("5. Exit System")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            product_manager_system()
        elif choice == '2':
            supplier_manager_system()
        elif choice == '3':
            purchase_order_system()
        elif choice == '4':
            stock_management_system()
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")