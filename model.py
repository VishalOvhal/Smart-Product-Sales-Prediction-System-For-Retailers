import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np

# Hybrid Model Class
class HybridModel:
    def __init__(self):
        self.arima = None
        self.rf = RandomForestRegressor()
        self.preprocessor = ColumnTransformer(
            transformers=[('cat', OneHotEncoder(), ['Item_Fat_Content', 'Item_Type', 'Outlet_Size', 'Store_Location'])],
            remainder='passthrough'
        )
    
    def fit(self, X, y):
        # Time Series Component
        self.arima = ARIMA(y, order=(1,1,1)).fit()
        
        # Feature-based Component
        X_processed = self.preprocessor.fit_transform(X)
        self.rf.fit(X_processed, y - self.arima.predict(start=0, end=len(y)-1))
        
    def predict(self, X):
        time_pred = self.arima.forecast(steps=1).values[0]
        X_processed = self.preprocessor.transform(X)
        feat_pred = self.rf.predict(X_processed)
        return time_pred + feat_pred[0]