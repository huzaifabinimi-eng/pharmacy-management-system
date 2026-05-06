import streamlit as st
import json
from datetime import datetime

# Set page config
st.set_page_config(page_title="Pharmacy Dashboard", layout="wide", initial_sidebar_state="expanded")

# Title
st.title("🏥 Pharmacy Management System")
st.markdown("---")

# Initialize session state (remember data while app is running)
if 'medicines' not in st.session_state:
    st.session_state.medicines = {}
if 'customers' not in st.session_state:
    st.session_state.customers = {}
if 'sales' not in st.session_state:
    st.session_state.sales = []

# Sidebar menu
menu = st.sidebar.radio("📋 Menu", ["🏠 Home", "💊 Add Medicine", "👥 Register Customer", "🛒 Sell Medicine", "📦 View Inventory", "💰 Sales Summary"])

# ===== HOME PAGE =====
if menu == "🏠 Home":
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Medicines", len(st.session_state.medicines), "types")
    with col2:
        st.metric("Total Customers", len(st.session_state.customers), "registered")
    with col3:
        st.metric("Total Sales", len(st.session_state.sales), "transactions")
    with col4:
        total_revenue = sum([sale['total'] for sale in st.session_state.sales])
        st.metric("Total Revenue", f"${total_revenue:.2f}", "earned")
    
    st.markdown("---")
    st.info("👉 Use the menu on the left to manage your pharmacy!")

# ===== ADD MEDICINE =====
elif menu == "💊 Add Medicine":
    st.subheader("Add New Medicine")
    
    col1, col2 = st.columns(2)
    
    with col1:
        med_id = st.text_input("Medicine ID", placeholder="e.g., MED001")
        name = st.text_input("Medicine Name", placeholder="e.g., Aspirin")
        quantity = st.number_input("Quantity", min_value=0, value=0)
    
    with col2:
        price = st.number_input("Price ($)", min_value=0.0, value=0.0, step=0.01)
        expiry_date = st.date_input("Expiry Date")
    
    if st.button("✅ Add Medicine", key="add_med"):
        if not med_id or not name:
            st.error("❌ Please fill all fields!")
        elif med_id in st.session_state.medicines:
            st.error("❌ Medicine ID already exists!")
        else:
            st.session_state.medicines[med_id] = {
                "name": name,
                "quantity": quantity,
                "price": price,
                "expiry_date": str(expiry_date)
            }
            st.success(f"✅ Medicine '{name}' added successfully!")
            st.balloons()

# ===== REGISTER CUSTOMER =====
elif menu == "👥 Register Customer":
    st.subheader("Register New Customer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cust_id = st.text_input("Customer ID", placeholder="e.g., CUST001")
        name = st.text_input("Customer Name", placeholder="e.g., Ali")
    
    with col2:
        allergies = st.text_input("Allergies (or 'None')", placeholder="e.g., Penicillin")
    
    if st.button("✅ Register Customer", key="add_cust"):
        if not cust_id or not name:
            st.error("❌ Please fill all fields!")
        elif cust_id in st.session_state.customers:
            st.error("❌ Customer ID already exists!")
        else:
            st.session_state.customers[cust_id] = {
                "name": name,
                "allergies": allergies
            }
            st.success(f"✅ Customer '{name}' registered successfully!")
            st.balloons()

# ===== SELL MEDICINE =====
elif menu == "🛒 Sell Medicine":
    st.subheader("Process Sale")
    
    if not st.session_state.medicines or not st.session_state.customers:
        st.error("❌ Please add medicines and customers first!")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            customer_list = [f"{cid}: {c['name']}" for cid, c in st.session_state.customers.items()]
            selected_customer = st.selectbox("Select Customer", customer_list)
            cust_id = selected_customer.split(":")[0]
            
            medicine_list = [f"{mid}: {m['name']}" for mid, m in st.session_state.medicines.items()]
            selected_medicine = st.selectbox("Select Medicine", medicine_list)
            med_id = selected_medicine.split(":")[0]
        
        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1)
        
        if st.button("🛒 Complete Sale", key="sell"):
            medicine = st.session_state.medicines[med_id]
            
            if medicine['quantity'] < quantity:
                st.error(f"❌ Insufficient stock! Available: {medicine['quantity']}")
            else:
                total = medicine['price'] * quantity
                medicine['quantity'] -= quantity
                
                st.session_state.sales.append({
                    "customer": st.session_state.customers[cust_id]['name'],
                    "medicine": medicine['name'],
                    "quantity": quantity,
                    "total": total,
                    "date": str(datetime.now())
                })
                
                st.success("✅ Sale completed successfully!")
                
                # Display receipt
                st.markdown("---")
                st.subheader("📄 Receipt")
                receipt_col1, receipt_col2 = st.columns([1, 1])
                with receipt_col1:
                    st.write(f"**Customer:** {st.session_state.customers[cust_id]['name']}")
                    st.write(f"**Medicine:** {medicine['name']}")
                with receipt_col2:
                    st.write(f"**Quantity:** {quantity}")
                    st.write(f"**Total:** ${total:.2f}")
                st.balloons()

# ===== VIEW INVENTORY =====
elif menu == "📦 View Inventory":
    st.subheader("Current Inventory")
    
    if not st.session_state.medicines:
        st.info("📭 No medicines in inventory")
    else:
        # Create a table
        inventory_data = []
        for med_id, med in st.session_state.medicines.items():
            inventory_data.append({
                "ID": med_id,
                "Name": med['name'],
                "Quantity": med['quantity'],
                "Price": f"${med['price']:.2f}",
                "Expiry Date": med['expiry_date']
            })
        
        st.dataframe(inventory_data, use_container_width=True, hide_index=True)

# ===== SALES SUMMARY =====
elif menu == "💰 Sales Summary":
    st.subheader("Sales Summary")
    
    if not st.session_state.sales:
        st.info("📭 No sales yet")
    else:
        # Sales table
        st.write("**Recent Sales:**")
        sales_data = []
        for sale in st.session_state.sales:
            sales_data.append({
                "Customer": sale['customer'],
                "Medicine": sale['medicine'],
                "Quantity": sale['quantity'],
                "Total": f"${sale['total']:.2f}",
                "Date": sale['date']
            })
        
        st.dataframe(sales_data, use_container_width=True, hide_index=True)
        
        # Summary stats
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Transactions", len(st.session_state.sales))
        with col2:
            total_revenue = sum([sale['total'] for sale in st.session_state.sales])
            st.metric("Total Revenue", f"${total_revenue:.2f}")
        with col3:
            total_items_sold = sum([sale['quantity'] for sale in st.session_state.sales])
            st.metric("Total Items Sold", total_items_sold)