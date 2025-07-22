import csv
import os

class Product:
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

    def get_all_products(self):
        return self.products

    def search_product(self, product_name):
        for product in self.products:
            if product['name'].lower() == product_name.lower():
                return product
        return None

    def add_product(self, product):
        self.products.append(product)
        self.save_products()

    def update_product(self, product_name, updated_product):
        for i, product in enumerate(self.products):
            if product['name'].lower() == product_name.lower():
                self.products[i] = updated_product
                self.save_products()
                return True
        return False

    def delete_product(self, product_name):
        self.products = [p for p in self.products if p['name'].lower() != product_name.lower()]
        self.save_products()

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