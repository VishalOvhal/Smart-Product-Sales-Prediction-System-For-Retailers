import streamlit as st
import pandas as pd
import joblib

def get_recommendations(predicted_sales):
    if predicted_sales < 1000:
        return ["Lower the price by 10%", "Increase social media ads"]
    else:
        return ["Bundle with accessories", "Target premium customer segments"]

def main():
    st.title("Future Product Sales Prediction")
    
    # Load model
    model = joblib.load('new_product_model.pkl')
    
    # Input form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        price = col1.number_input("Price", min_value=0.0, value=100.0)
        buzz = col2.number_input("Social Media Buzz Score", min_value=0.0, value=50.0)
        
        category = st.selectbox("Category", options=[
            'Health_and_Hygiene', 'Soft_Drinks', 'Dairy',
            'Fruits_and_Vegetables', 'Baking_Goods', 'Canned',
            'Breakfast', 'Meat', 'Snaks_Foods', 'Other'
        ])
        
        submitted = st.form_submit_button("Predict Sales")
    
    # Prediction logic
    if submitted:
        input_data = pd.DataFrame({
            'price': [price],
            'social_media_buzz': [buzz],
            'competitor_price': [price * 0.9],
            'category_Health_and_Hygiene': [1 if category == 'Health_and_Hygiene' else 0],
            'category_Soft_Drinks': [1 if category == 'Soft_Drinks' else 0],
            'category_Dairy': [1 if category == 'Dairy' else 0],
            'category_Fruits_and_Vegetables': [1 if category == 'Fruits_and_Vegetables' else 0],
            'category_Baking_Goods': [1 if category == 'Baking_Goods' else 0],
            'category_Canned': [1 if category == 'Canned' else 0],
            'category_Breakfast': [1 if category == 'Breakfast' else 0],
            'category_Meat': [1 if category == 'Meat' else 0],
            'category_Snaks_Foods': [1 if category == 'Snaks_Foods' else 0],
            'category_Other': [1 if category == 'Other' else 0]
        }).reindex(columns=model.feature_names_in_, fill_value=0)
        
        prediction = model.predict(input_data)[0]
        
        # Display results
        st.subheader(f"Predicted Sales: {int(prediction)} units")
        st.markdown("### Recommendations")
        for recommendation in get_recommendations(prediction):
            st.markdown(f"- {recommendation}")