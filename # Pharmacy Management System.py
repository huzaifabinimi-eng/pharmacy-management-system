# Pharmacy Management System
# Uses: Functions, Data Structures (Lists, Dictionaries), Loops, Conditionals, 
# File I/O, Exception Handling, OOP

class Medicine:
    """Represents a Medicine in the pharmacy"""
    def __init__(self, medicine_id, name, quantity, price, expiry_date):
        self.medicine_id = medicine_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.expiry_date = expiry_date
    
    def __str__(self):
        return f"ID: {self.medicine_id}, Name: {self.name}, Qty: {self.quantity}, Price: ${self.price}, Expiry: {self.expiry_date}"


class Customer:
    """Represents a Customer"""
    def __init__(self, customer_id, name, allergies="None"):
        self.customer_id = customer_id
        self.name = name
        self.allergies = allergies
    
    def __str__(self):
        return f"ID: {self.customer_id}, Name: {self.name}, Allergies: {self.allergies}"


class PharmacyManagementSystem:
    """Main Pharmacy Management System"""
    
    def __init__(self):
        self.medicines = {}  # Dictionary: {medicine_id: Medicine}
        self.customers = {}  # Dictionary: {customer_id: Customer}
        self.sales = []      # List of sales transactions
        self.load_data()
    
    # ===== INVENTORY MANAGEMENT =====
    def add_medicine(self):
        """Add a new medicine to inventory"""
        try:
            med_id = input("Enter Medicine ID: ").strip()
            if med_id in self.medicines:
                print("❌ Medicine ID already exists!")
                return
            
            name = input("Enter Medicine Name: ").strip()
            quantity = int(input("Enter Quantity: "))
            price = float(input("Enter Price: "))
            expiry = input("Enter Expiry Date (YYYY-MM-DD): ").strip()
            
            self.medicines[med_id] = Medicine(med_id, name, quantity, price, expiry)
            print(f"✅ Medicine '{name}' added successfully!")
        
        except ValueError:
            print("❌ Invalid input! Please enter correct data types.")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def update_inventory(self):
        """Update medicine quantity"""
        try:
            med_id = input("Enter Medicine ID: ").strip()
            if med_id not in self.medicines:
                print("❌ Medicine not found!")
                return
            
            quantity = int(input("Enter new quantity: "))
            self.medicines[med_id].quantity = quantity
            print("✅ Inventory updated!")
        
        except ValueError:
            print("❌ Invalid input!")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def check_expiry_dates(self):
        """Check and display expired medicines"""
        print("\n📋 Expired Medicines:")
        expired = [med for med in self.medicines.values() if med.expiry_date <= "2026-04-27"]
        
        if not expired:
            print("✅ No expired medicines!")
        else:
            for med in expired:
                print(f"  - {med.name} (ID: {med.medicine_id}) - Expiry: {med.expiry_date}")
    
    def check_low_stock(self, threshold=5):
        """Check medicines with low stock"""
        print(f"\n⚠️  Low Stock Medicines (below {threshold}):")
       
        low_stock = [med for med in self.medicines.values() if med.quantity < threshold]
        
        if not low_stock:
            print("✅ All medicines in stock!")
        else:
            for med in low_stock:
                print(f"  - {med.name}: {med.quantity} units")
    
    # ===== CUSTOMER MANAGEMENT =====
    def register_customer(self):
        """Register a new customer"""
        try:
            cust_id = input("Enter Customer ID: ").strip()
            if cust_id in self.customers:
                print("❌ Customer ID already exists!")
                return
            
            name = input("Enter Customer Name: ").strip()
            allergies = input("Enter Allergies (or 'None'): ").strip()
            
            self.customers[cust_id] = Customer(cust_id, name, allergies)
            print(f"✅ Customer '{name}' registered successfully!")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def check_allergies(self):
        """Check customer allergies before dispensing"""
        cust_id = input("Enter Customer ID: ").strip()
        if cust_id not in self.customers:
            print("❌ Customer not found!")
            return
        
        customer = self.customers[cust_id]
        print(f"\n⚠️  Customer: {customer.name}")
        print(f"Allergies: {customer.allergies}")
    
    # ===== SALES & BILLING =====
    def sell_medicine(self):
        """Process a sale transaction"""
        try:
            cust_id = input("Enter Customer ID: ").strip()
            if cust_id not in self.customers:
                print("❌ Customer not found!")
                return
            
            med_id = input("Enter Medicine ID: ").strip()
            if med_id not in self.medicines:
                print("❌ Medicine not found!")
                return
            
            quantity = int(input("Enter Quantity to Sell: "))
            medicine = self.medicines[med_id]
            
            if medicine.quantity < quantity:
                print("❌ Insufficient stock!")
                return
            
            # Calculate total
            total_price = medicine.price * quantity
            medicine.quantity -= quantity
            
            # Record sale
            sale = {
                "customer": self.customers[cust_id].name,
                "medicine": medicine.name,
                "quantity": quantity,
                "total": total_price
            }
            self.sales.append(sale)
            
            print(f"\n✅ Sale Completed!")
            print(f"Medicine: {medicine.name}")
            print(f"Quantity: {quantity}")
            print(f"Total: ${total_price:.2f}")
        
        except ValueError:
            print("❌ Invalid input!")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def generate_receipt(self):
        """Generate and display a receipt"""
        if not self.sales:
            print("❌ No sales records!")
            return
        
        last_sale = self.sales[-1]
        print("\n" + "="*40)
        print("           PHARMACY RECEIPT")
        print("="*40)
        print(f"Customer: {last_sale['customer']}")
        print(f"Medicine: {last_sale['medicine']}")
        print(f"Quantity: {last_sale['quantity']}")
        print(f"Total Amount: ${last_sale['total']:.2f}")
        print("="*40 + "\n")
    
    # ===== SALES ANALYTICS =====
    def display_sales_report(self):
        """Display sales trends"""
        if not self.sales:
            print("❌ No sales records!")
            return
        
        print("\n📊 Sales Report:")
        total_revenue = 0
        for i, sale in enumerate(self.sales, 1):
            print(f"{i}. {sale['customer']} - {sale['medicine']}: ${sale['total']:.2f}")
            total_revenue += sale['total']
        
        print(f"\nTotal Revenue: ${total_revenue:.2f}")
        print(f"Total Transactions: {len(self.sales)}")
    
    def display_inventory(self):
        """Display all medicines in inventory"""
        if not self.medicines:
            print("❌ No medicines in inventory!")
            return
        
        print("\n📦 Current Inventory:")
        for med in self.medicines.values():
            print(f"  {med}")
    
    # ===== FILE I/O =====
    def save_data(self):
        """Save data to files"""
        try:
            # Save medicines
            with open("medicines.txt", "w") as f:
                for med in self.medicines.values():
                    f.write(f"{med.medicine_id}|{med.name}|{med.quantity}|{med.price}|{med.expiry_date}\n")
            
            # Save customers
            with open("customers.txt", "w") as f:
                for cust in self.customers.values():
                    f.write(f"{cust.customer_id}|{cust.name}|{cust.allergies}\n")
            
            # Save sales
            with open("sales.txt", "w") as f:
                for sale in self.sales:
                    f.write(f"{sale['customer']}|{sale['medicine']}|{sale['quantity']}|{sale['total']}\n")
            
            print("✅ Data saved successfully!")
        
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def load_data(self):
        """Load data from files"""
        try:
            # Load medicines
            with open("medicines.txt", "r") as f:
                for line in f:
                    data = line.strip().split("|")
                    if len(data) == 5:
                        med_id, name, qty, price, expiry = data
                        self.medicines[med_id] = Medicine(med_id, name, int(qty), float(price), expiry)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"⚠️  Error loading medicines: {e}")
        
        try:
            # Load customers
            with open("customers.txt", "r") as f:
                for line in f:
                    data = line.strip().split("|")
                    if len(data) == 3:
                        cust_id, name, allergies = data
                        self.customers[cust_id] = Customer(cust_id, name, allergies)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"⚠️  Error loading customers: {e}")
        
        try:
            # Load sales
            with open("sales.txt", "r") as f:
                for line in f:
                    data = line.strip().split("|")
                    if len(data) == 4:
                        self.sales.append({
                            "customer": data[0],
                            "medicine": data[1],
                            "quantity": int(data[2]),
                            "total": float(data[3])
                        })
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"⚠️  Error loading sales: {e}")
    
    # ===== MAIN MENU =====
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("    🏥 PHARMACY MANAGEMENT SYSTEM 🏥")
        print("="*50)
        print("1. Add Medicine")
        print("2. Update Inventory")
        print("3. Check Expiry Dates")
        print("4. Check Low Stock")
        print("5. Register Customer")
        print("6. Check Customer Allergies")
        print("7. Sell Medicine (Billing)")
        print("8. Generate Receipt")
        print("9. Display Sales Report")
        print("10. Display Inventory")
        print("11. Save Data")
        print("12. Exit")
        print("="*50)
    
    def run(self):
        """Main application loop"""
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-12): ").strip()
            
            if choice == "1":
                self.add_medicine()
            elif choice == "2":
                self.update_inventory()
            elif choice == "3":
                self.check_expiry_dates()
            elif choice == "4":
                self.check_low_stock()
            elif choice == "5":
                self.register_customer()
            elif choice == "6":
                self.check_allergies()
            elif choice == "7":
                self.sell_medicine()
            elif choice == "8":
                self.generate_receipt()
            elif choice == "9":
                self.display_sales_report()
            elif choice == "10":
                self.display_inventory()
            elif choice == "11":
                self.save_data()
            elif choice == "12":
                self.save_data()
                print("👋 Thank you for using Pharmacy Management System!")
                break
            else:
                print("❌ Invalid choice! Please try again.")


# Entry Point
if __name__ == "__main__":
    system = PharmacyManagementSystem()
    system.run()
