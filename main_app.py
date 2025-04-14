import streamlit as st
import product
import sales
import supplier
import item_supply
import new_product_prediction
import database as db
import hashlib



def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(input_password, hashed_password):
    return hash_password(input_password) == hashed_password



def show_login():
    st.subheader("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    
    if st.button("Login"):
        user = db.get_user(username)
        if user:
            # Access the password using the tuple index (index 1 for the password)
            if check_password(password, user['password']): 
                st.session_state.authenticated = True
                st.session_state.username = username
                #st.experimental_rerun()
            else:
                st.error("Invalid password")
        else:
            st.error("Username not found")

def show_register():
    st.subheader("Register")
    new_user = st.text_input("New Username", key="reg_user")
    new_pass = st.text_input("New Password", type="password", key="reg_pass")
    confirm_pass = st.text_input("Confirm Password", type="password", key="conf_pass")
    
    if st.button("Create Account"):
        if new_pass != confirm_pass:
            st.error("Passwords do not match")
        elif db.get_user(new_user):
            st.error("Username already exists")
        else:
            hashed_pass = hash_password(new_pass)
            db.create_user(new_user, hashed_pass)
            st.success("Account created! Please login")

def show_login_register():
    st.title("Welcome to Smart Selling Prediction System")
    choice = st.radio("Choose Option", ["Login", "Register"])
    
    if choice == "Login":
        show_login()
    else:
        show_register()




# main app code 


def main_app():
    st.sidebar.title("Smart Selling Prediction System")
    
    # Add logout button
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.experimental_rerun()
    

    choice = st.sidebar.radio(
        "Go to",
        ("📦 Product Management", "🤝 Supplier Management", 
         "🚚 Item Supply Management", "📈 Sales Prediction", "📈 New Product Prediction"),
        label_visibility="collapsed"
    )

    if choice == "📦 Product Management":
        product.main()
    elif choice == "🤝 Supplier Management":
        supplier.main()
    elif choice == "🚚 Item Supply Management":
        item_supply.main()
    elif choice == "📈 Sales Prediction":
        sales.main()
    elif choice == "📈 New Product Prediction":
        new_product_prediction.main()
    else:
        show_dashboard()

def show_dashboard():
    st.title("Inventory Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Products", len(db.get_product()))
    with col2:
        st.metric("Active Suppliers", len(db.get_supplier()))
    with col3:
        stock_info = db.get_supply_info()['ITEM_Stocks'].sum()
        st.metric("Total Stock Units", stock_info)




def main():
    if 'db_initialized' not in st.session_state:
        db.init_db()  
        st.session_state.db_initialized = True

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login_register()
    else:
        main_app()

if __name__ == "__main__":
    main()