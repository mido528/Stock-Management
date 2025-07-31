import csv
import os

class Supplier:
    def __init__(self, file_path):
        self.file_path = file_path
        self.suppliers = self.load_suppliers()

    def load_suppliers(self):
        suppliers = []
        if os.path.exists(self.file_path):
            with open(self.file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    suppliers.append({
                        'name': row['Name'],
                        'supplier_contact_information': row['Supplier_Contact_Information'],
                        'supplier_product_category': row['Supplier_Product_Category']
                    })
        return suppliers

    def get_all_suppliers(self):
        return self.suppliers

    def search_supplier(self, supplier_name):
        for supplier in self.suppliers:
            if supplier['name'].lower() == supplier_name.lower():
                return supplier
        return None

    def add_supplier(self, supplier):
        self.suppliers.append(supplier)
        self.save_supplier()

    def update_supplier(self, supplier_name, updated_supplier):
        for i, supplier in enumerate(self.suppliers):
            if supplier['name'].lower() == supplier_name.lower():
                self.suppliers[i] = updated_supplier
                self.save_supplier()
                return True
        return False

    def delete_supplier(self, supplier_name):
        self.suppliers = [s for s in self.suppliers if s['name'].lower() != supplier_name.lower()]
        self.save_supplier()

    def save_supplier(self):
        with open(self.file_path, mode='w', newline='') as file:
            fieldnames = ['Name', 'Supplier_Contact_Information', 'Supplier_Product_Category']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for supplier in self.suppliers:
                writer.writerow({
                    'Name': supplier['name'],
                    'Supplier_Contact_Information': supplier['supplier_contact_information'],
                    'Supplier_Product_Category': supplier['supplier_product_category']
                })