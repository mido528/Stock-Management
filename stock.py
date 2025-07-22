import csv
import os

class Stock:
    def __init__(self, file_path):
        self.file_path = file_path
        self.products = self.load_products()

    def load_products(self):
        products = []
        if os.path.exists(self.file_path):
            with open(self.file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    products.append({
                        'name': row['Name'],
                        'price': float(row['Price']),
                        'quantity': int(row['Quantity'])
                    })
        return products

    def search_product(self, product_name):
        for product in self.products:
            if product['name'].lower() == product_name.lower():
                return product
        return None

    def receive_stock(self, product_name, quantity):
        for product in self.products:
            if product['name'].lower() == product_name.lower():
                product['quantity'] += quantity
                self.save_products()
                return True
        return False

    def record_sale(self, product_name, quantity):
        for product in self.products:
            if product['name'].lower() == product_name.lower():
                if product['quantity'] >= quantity:
                    product['quantity'] -= quantity
                    self.save_products()
                    return True
                else:
                    return False
        return False

    def adjust_stock(self, product_name, new_quantity, reason):
        for product in self.products:
            if product['name'].lower() == product_name.lower():
                product['quantity'] = new_quantity
                self.save_products()
                return True
        return False

    def generate_stock_report(self):
        print("\nStock Report:")
        print("{:<30} {:<10} {:<10}".format("Product Name", "Price", "Quantity"))
        print("-" * 50)
        for product in self.products:
            print("{:<30} £{:<9.2f} {:<10}".format(
                product['name'], product['price'], product['quantity']))

    def save_products(self):
        with open(self.file_path, mode='w', newline='') as file:
            fieldnames = ['Name', 'Price', 'Quantity']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for product in self.products:
                writer.writerow({
                    'Name': product['name'],
                    'Price': product['price'],
                    'Quantity': product['quantity']
                })