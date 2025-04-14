import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
import joblib


def generate_mock_data():
    np.random.seed(42)
    data = {
        'product_id': np.arange(100),
        'price': np.random.uniform(10, 500, 100),
        'category': np.random.choice(['Health_and_Hygiene', 'Soft_Drinks', 'Dairy', 'Fruits_and_Vegetables', 'Baking_Goods', 'Canned', 'Breakfast', 'Meat', 'Snaks_Foods', 'Other'], 100),
        'social_media_buzz': np.random.normal(50, 10, 100),
        'competitor_price': np.random.uniform(10, 500, 100),
        'sales': np.random.randint(100, 5000, 100)
    }
    return pd.DataFrame(data)

# Preprocess data
def preprocess_data(df):
    df = pd.get_dummies(df, columns=['category'])
    scaler = StandardScaler()
    features = ['price', 'social_media_buzz', 'competitor_price']
    df[features] = scaler.fit_transform(df[features])
    return df

# Train model
def train_model():
    df = generate_mock_data()
    df = preprocess_data(df)
    
    X = df.drop(['sales', 'product_id'], axis=1)
    y = df['sales']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    model = XGBRegressor()
    model.fit(X_train, y_train)
    
    # Save model and scaler
    joblib.dump(model, 'new_product_model.pkl')
    print("Model trained and saved!")

if __name__ == "__main__":
    train_model()