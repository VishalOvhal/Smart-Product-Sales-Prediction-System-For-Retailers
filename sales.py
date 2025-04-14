import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model import HybridModel

# Load and preprocess data
df = pd.read_csv('Grocery_data_from_2020-2024.csv')
years = ['Sales_in_2020', 'Sales_in_2021', 'Sales_in_2022', 'Sales_in_2023', 'Sales_in_2024']

# Train model
def train_model():
    melted = pd.melt(df, id_vars=[col for col in df.columns if col not in years], 
                    value_vars=years, var_name='Year', value_name='Sales')
    melted['Year'] = melted['Year'].str[-4:].astype(int)
    
    X = melted[['Item_Weight', 'Item_Fat_Content', 'Item_Visibility', 'Item_Type', 
               'Item_MRP', 'Outlet_Size', 'Store_Location', 'Year']]
    y = melted['Sales']
    
    model = HybridModel()
    model.fit(X, y)
    return model

model = train_model()

# Main function for sales prediction
def main():
    st.title("📈 Sales Prediction")
    
    product_id = st.text_input("Enter Product ID:", placeholder="e.g., ITEM_1")
    predict_btn = st.button("Predict Future Sales")

    if predict_btn and product_id:
        try:
            product_data = df[df['Item_Identifier'] == product_id].iloc[0]
            historical = product_data[years].values.astype(int)
            
            # Prepare input for prediction
            X_new = pd.DataFrame([{
                'Item_Weight': product_data['Item_Weight'],
                'Item_Fat_Content': product_data['Item_Fat_Content'],
                'Item_Visibility': product_data['Item_Visibility'],
                'Item_Type': product_data['Item_Type'],
                'Item_MRP': product_data['Item_MRP'],
                'Outlet_Size': product_data['Outlet_Size'],
                'Store_Location': product_data['Store_Location'],
                'Year': 2025
            }])
            
            # Make prediction
            pred_2025 = int(model.predict(X_new))
            
            # Display results
            st.subheader(f"Prediction Result for {product_id}")
            col1, col2 = st.columns(2)
            col1.metric("Predicted 2025 Sales", f"{pred_2025} units")
            col2.metric("2024 Sales", f"{historical[-1]} units", 
                       delta=f"{(pred_2025 - historical[-1])/historical[-1]:.1%}")
            
            # Visualization
            st.subheader("Sales Trend Analysis")
            fig, ax = plt.subplots()
            years_list = [2020, 2021, 2022, 2023, 2024, 2025]
            values = list(historical) + [pred_2025]
            ax.plot(years_list, values, marker='o', linestyle='--')
            ax.set_xlabel("Year")
            ax.set_ylabel("Sales Units")
            ax.set_title("Historical vs Predicted Sales")
            ax.grid(True)
            st.pyplot(fig)
            
            # Suggestions
            st.subheader("Optimization Recommendations")
            if pred_2025 < historical[-1]:
                st.warning("Sales Decline Detected - Action Needed:")
                suggestions = [
                    "🚀 Launch targeted promotions for underperforming regions",
                    "📊 Conduct market basket analysis to improve product placement",
                    "💰 Optimize pricing strategy based on competitor analysis",
                    "📢 Increase digital marketing spend by 15-20%",
                    "🎯 Implement customer loyalty programs for repeat purchases"
                ]
                for suggestion in suggestions:
                    st.markdown(f"- {suggestion}")
            else:
                st.success("Positive Growth Trend Detected - Maintain Momentum:")
                st.markdown("- Continue current successful strategies")
                st.markdown("- Explore market expansion opportunities")
                st.markdown("- Consider inventory optimization for predicted demand")
                
        except IndexError:
            st.error("⚠️ Product ID not found. Please check and try again.")