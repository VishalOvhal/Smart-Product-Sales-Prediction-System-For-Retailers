import streamlit as st
import database as db

def main():
    st.title("📦 Product Management")

    
    with st.form("product_form"):
        col0, col1= st.columns(2)
        with col0:
            item_id = st.text_input("**ITEM ID**", 
                                  help="Unique product identifier")
            existing_ids = db.get_product()['ITEM_ID'].tolist()
            if item_id in existing_ids:
                st.warning("⚠️ This ID already exists!")

            item_mrp = st.number_input("ITEM MRP", min_value=0)
            item_type = st.text_input("ITEM Type")
            item_weight = st.number_input("ITEM Weight (gram)", min_value=0)

        with col1:
            item_name = st.text_input("ITEM Name")
            item_fat = st.selectbox("ITEM Fat Content", ["Very Low","Low", "Regular", "High", "Very High"])
            item_details = st.text_area("ITEM Details")

        col_add, col_update, col_delete = st.columns(3)
        with col_add:
            add_clicked = st.form_submit_button("➕ Add")
        # with col_clear:
        #     clear_clicked = st.form_submit_button("🔄 Clear")
        with col_update:
            update_clicked = st.form_submit_button("✏️ Update")
        with col_delete:
            delete_clicked = st.form_submit_button("🗑️ Delete")
        


        # Handle button actions
        if add_clicked:
            if item_id:
                try:
                    db.add_product(
                        item_id, item_name, item_weight,
                        item_fat, item_type, item_mrp, item_details
                    )
                    st.success("Product added successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("ITEM ID is required!")


        # if clear_clicked:
        #     st.item_id = set(''),
        #     st.item_mrp = set(''),
        #     st.item_type = set(''),
        #     st.item_weight = set(''),
        #     st.item_name = set(''),
        #     st.item_fat = set(''),
        #     st.item_details = set('')
            
            
        if update_clicked:
            try:
                db.update_product(item_id,
                    item_name, item_weight, item_fat, 
                    item_type, item_mrp, item_details
                )
                st.success("Product updated successfully!")
            except Exception as e:
                st.error(f"Error updating: {e}")
                
        if delete_clicked:
            try:
                db.delete_product(item_id)
                st.success("ITEM deleted successfully!")
            except Exception as e:
                st.error(f"Error deleting: {e}")

    
    # st.subheader("Product List")
    # products = db.get_product()
    # st.dataframe(products)
    
    
    st.subheader("Product Inventory")
    products = db.get_product()
    edited_df = st.data_editor(
        products,
        column_config={
            "ITEM_MRP": st.column_config.NumberColumn(
                format="₹%d",
                help="Maximum Retail Price"
            )
        },
        use_container_width=True
    )
