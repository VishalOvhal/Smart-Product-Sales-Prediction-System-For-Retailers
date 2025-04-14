import streamlit as st
import database as db

def main():
    st.title("🤝 Supplier Management")
    

    with st.form("supplier_form"):
        col1, col2 = st.columns(2)
        with col1:
            sup_id = st.text_input("**Supplier ID**",
                                 help="Unique product identifier")
            existing_ids = db.get_product()['ITEM_ID'].tolist()
            if sup_id in existing_ids:
                st.warning("⚠️ This ID already exists!")
            
            sup_name = st.text_input("Supplier Name")
            contact = st.text_input("Contact Number")

        with col2:
            email = st.text_input("Email")
            address = st.text_area("Address")

        # Buttons
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
            if sup_id and sup_name:
                try:
                    db.add_supplier(sup_id, sup_name, contact, email, address)
                    st.success("Supplier added successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Supplier ID and Name are required!")
                
        # if clear_clicked:
        #     sup_id = set(''),
        #     sup_name = set(''),
        #     contact = set(''),
        #     email = set(''),
        #     address = set(''),
        
            
        if update_clicked:
            try:
                db.update_supplier(
                    sup_id,
                    sup_name, contact, email, address
                )
                st.success("Supplier updated successfully!")
            except Exception as e:
                st.error(f"Error updating: {e}")
                
        if delete_clicked:
            try:
                db.delete_supplier(sup_id)
                st.success("Supplier deleted successfully!")
            except Exception as e:
                st.error(f"Error deleting: {e}")


    # Supplier List and Selection
    st.subheader("📋 Supplier List")
    suppliers = db.get_supplier()
    
    if not suppliers.empty:
        # Display interactive dataframe
        selected_sup = st.selectbox(
            "Select Supplier from List:",
            options=suppliers['Supplier_ID'],
            format_func=lambda x: f"{x} - {suppliers[suppliers['Supplier_ID'] == x]['Supplier_Name'].iloc[0]}",
            index=None
        )

        # Populate form when supplier is selected
        if selected_sup:
            selected_data = suppliers[suppliers['Supplier_ID'] == selected_sup].iloc[0]
            st.session_state.sup_id = selected_sup
            st.session_state.form_data = {
                'sup_id': selected_data['Supplier_ID'],
                'sup_name': selected_data['Supplier_Name'],
                'contact': selected_data['Contact_Number'],
                'email': selected_data['Email'],
                'address': selected_data['Address']
            }
            st.rerun()
            
        st.dataframe(suppliers, use_container_width=True)
    else:
        st.info("No suppliers found in database")

if __name__ == "__main__":
    main()