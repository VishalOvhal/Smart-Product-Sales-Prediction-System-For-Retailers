import streamlit as st
import database as db

def main():
    st.title("🚚 Item Supply Management")
    
    db.create_item_stock_table()
    
    products = db.get_product()
    suppliers = db.get_supplier()
    
    with st.form("supply_form"):
        item_id = st.selectbox("Select ITEM ID", products['ITEM_ID'])
        sup_id = st.selectbox("Select Supplier ID", suppliers['Supplier_ID'])
        stocks = st.number_input("Stocks", min_value=0)

        mfd, exp = st.columns(2)
        mfd = st.date_input("Manufacturing Date")
        exp = st.date_input("Expiry Date")


        # Buttons
        col_add, col_update, col_delete = st.columns(3)
        with col_add:
            add_clicked = st.form_submit_button("➕ Add")
        with col_update:
            update_clicked = st.form_submit_button("✏️ Update")
        with col_delete:
            delete_clicked = st.form_submit_button("🗑️ Delete")


        # Handle button actions
        if add_clicked:
            if sup_id:
                try:
                    db.add_supply_info(item_id, sup_id, stocks, mfd, exp)
                    st.success("Supplier added successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Supplier ID and Name are required!")
        
            
        if update_clicked:
            try:
                db.update_supply_info(
                    item_id,
                     stocks, mfd, exp
                )
                st.success("Stock info updated successfully!")
            except Exception as e:
                st.error(f"Error updating: {e}")
                
        if delete_clicked:
            try:
                db.delete_supply_info(item_id)
                st.success("Stock info deleted successfully!")
            except Exception as e:
                st.error(f"Error deleting: {e}")


    st.subheader("Current Supply Information")
    supply_info = db.get_supply_info()
    st.dataframe(supply_info)