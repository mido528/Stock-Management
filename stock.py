import csv
import os
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    quantity: int

class Stock:
    def __init__(self, file_path):
        self.file_path = file_path
        self.products = self.load_products()

    def load_products(self):
        products = []
        if not os.path.exists(self.file_path):
            return products
        
        with open(self.file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                products.append(Product(
                    name=row['Name'],
                    price=float(row['Price']),
                    quantity=int(row['Quantity'])
                ))
        return products

    def save_products(self):
        with open(self.file_path, mode='w', newline='') as file:
            fieldnames = ['Name', 'Price', 'Quantity']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for product in self.products:
                writer.writerow({
                    'Name': product.name,
                    'Price': product.price,
                    'Quantity': product.quantity
                })

    def search_product(self, product_name):
        for product in self.products:
            if product.name.lower() == product_name.lower():
                return product
        return None

    def receive_stock(self, product_name, quantity):
        product = self.search_product(product_name)
        if product:
            product.quantity += quantity
            self.save_products()
            return True
        return False

    def record_sale(self, product_name, quantity):
        product = self.search_product(product_name)
        if product and product.quantity >= quantity:
            product.quantity -= quantity
            self.save_products()
            return True
        return False

    def adjust_stock(self, product_name, new_quantity):
        product = self.search_product(product_name)
        if product:
            product.quantity = new_quantity
            self.save_products()
            return True
        return False

    def generate_stock_report(self):
        print("\n--- Stock Report ---")
        print(f"{'Product Name':<30} {'Price':<10} {'Quantity':<10}")
        print("-" * 50)
        for product in self.products:
            print(f"{product.name:<30} £{product.price:<9.2f} {product.quantity:<10}")

if __name__ == '__main__':
    with open('stock.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Price', 'Quantity'])
        writer.writerow(['Laptop', 999.99, 10])
        writer.writerow(['Mouse', 24.50, 50])
        writer.writerow(['Keyboard', 75.00, 30])

    stock_manager = Stock('stock.csv')
    stock_manager.generate_stock_report()

    print("\nUpdating stock...")
    stock_manager.record_sale('Laptop', 2)
    stock_manager.receive_stock('Mouse', 100)
    
    stock_manager.generate_stock_report()
