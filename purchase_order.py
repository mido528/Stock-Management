import datetime

class PurchaseOrder:
    def __init__(self, product_name, quantity):
        self.product_name = product_name
        self.quantity = quantity
        self.order_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
    def generate_order(self):
        # In a real system, this would save to a database or file
        print(f"\nGenerated Purchase Order:")
        print(f"Product: {self.product_name}")
        print(f"Quantity: {self.quantity}")
        print(f"Order Date: {self.order_date}")
        print("=" * 30)
        return True