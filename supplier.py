import csv
import os
from dataclasses import dataclass
@dataclass
class SupplierData:
   
    name: str
    contact_info: str
    product_category: str

class Supplier:

    def __init__(self, file_path):
        self.file_path = file_path
      
        self.suppliers = self.load_suppliers()

    def load_suppliers(self):
        suppliers = []
        if not os.path.exists(self.file_path):
            return suppliers
            
        with open(self.file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
               
                suppliers.append(SupplierData(
                    name=row['Name'],
                    contact_info=row['ContactInfo'],
                    product_category=row['ProductCategory']
                ))
        return suppliers

    def save_suppliers(self):
      
        with open(self.file_path, mode='w', newline='') as file:
        
            fieldnames = ['Name', 'ContactInfo', 'ProductCategory']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for supplier in self.suppliers:
                writer.writerow({
                    'Name': supplier.name,
                    'ContactInfo': supplier.contact_info,
                    'ProductCategory': supplier.product_category
                })

    def get_all_suppliers(self):
        return self.suppliers

    def search_supplier(self, supplier_name):
       
        for supplier in self.suppliers:
          
            if supplier.name.lower() == supplier_name.lower():
                return supplier
        return None

    def add_supplier(self, supplier_data):
       
        if not self.search_supplier(supplier_data.name):
            self.suppliers.append(supplier_data)
            self.save_suppliers()

    def delete_supplier(self, supplier_name):
        
        self.suppliers = [s for s in self.suppliers if s.name.lower() != supplier_name.lower()]
        self.save_suppliers()

# --- Simple Example Usage ---
if __name__ == '__main__':
   
    file_name = 'supplier.csv'
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'ContactInfo', 'ProductCategory'])
        writer.writerow(['Office Goods', 'contact@officegoods.com', 'Stationery'])

    # 2. Create an instance of the manager
    supplier_manager = Supplier(file_name)

    # 3. Add a new supplier using the SupplierData class
    new_supplier = SupplierData(name="Tech Parts", contact_info="sales@techparts.com", product_category="Electronics")
    supplier_manager.add_supplier(new_supplier)

    # 4. Print all suppliers to see the result
    print("Current Suppliers:")
    for s in supplier_manager.get_all_suppliers():
        print(f"- Name: {s.name}, Category: {s.product_category}")
