import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os
from pathlib import Path

class Toronto311Pipeline:
    def __init__(self, csv_path="../data/SR2025.csv"):
        self.csv_path = csv_path
        self.df = None
        self.model = None
        self.label_encoder = None
        self.feature_columns = None
        self.categorical_encoders = {}


    def load_and_clean_data(self):
        self.df = pd.read_csv(self.csv_path, encoding="latin1", on_bad_lines="skip")
        self.df.columns = self.df.columns.str.strip()
        
        print(f"Loaded {len(self.df)} records")
        print(f"Columns: {list(self.df.columns)}")
        
       
        essential_cols = ['Status', 'Service Request Type', 'Division', 'Ward', 'Creation Date']
        initial_count = len(self.df)
        self.df = self.df.dropna(subset=essential_cols)
        print(f"Removed {initial_count - len(self.df)} rows with missing essential data")
        
    
        self.df['Creation Date'] = pd.to_datetime(self.df['Creation Date'], errors='coerce')
        self.df = self.df.dropna(subset=['Creation Date'])
        
     
        self.df['Date'] = self.df['Creation Date'].dt.date
        self.df['Month'] = self.df['Creation Date'].dt.month
        self.df['Weekday'] = self.df['Creation Date'].dt.dayofweek
        self.df['Hour'] = self.df['Creation Date'].dt.hour
        self.df['DayOfWeek'] = self.df['Creation Date'].dt.day_name()
        
      
        self.df['Status'] = self.df['Status'].str.strip()
        
        print(f"Cleaned data: {len(self.df)} records remaining")

    def generate_chart_data(self):
        chart_data = {}
    
        daily_counts = self.df.groupby('Date').size().reset_index(name='count')
        daily_counts['Date'] = daily_counts['Date'].astype(str)
    
        chart_data["time_series"] = {
            "dates": daily_counts['Date'].tolist()[-30:],
            "counts": [int(x) for x in daily_counts['count'].tolist()[-30:]]
        }
        
      
        ward_counts = self.df['Ward'].value_counts().head(15)
        chart_data["ward_distribution"] = {
            "wards": ward_counts.index.tolist(),
            "counts": [int(x) for x in ward_counts.values.tolist()]
        }
        
        
        status_counts = self.df['Status'].value_counts()
        chart_data["status_distribution"] = {
            "statuses": status_counts.index.tolist(),
            "counts": [int(x) for x in status_counts.values.tolist()]
        }
        
        service_counts = self.df['Service Request Type'].value_counts().head(15)
        chart_data["service_types"] = {
            "types": service_counts.index.tolist(),
            "counts": [int(x) for x in service_counts.values.tolist()]
        }
        
        
        division_counts = self.df['Division'].value_counts().head(10)
        chart_data["division_distribution"] = {
            "divisions": division_counts.index.tolist(),
            "counts": [int(x) for x in division_counts.values.tolist()]
        }
        
        
        hourly_counts = self.df.groupby('Hour').size()
        chart_data["hourly_pattern"] = {
            "hours": list(range(24)),
            "counts": [int(hourly_counts.get(h, 0)) for h in range(24)]
        }
        
        return chart_data
    
    def train_ml_model(self): 
        completed_statuses = ['Closed', 'Completed']
        self.df['Completed'] = self.df['Status'].isin(completed_statuses).astype(int)
        
        print(f"Completion rate: {self.df['Completed'].mean():.2%}")
        
        
        categorical_features = ['Service Request Type', 'Division', 'Ward']
        
       
        feature_data = []
        
       
        for col in categorical_features:
            encoded = pd.get_dummies(self.df[col], prefix=col, drop_first=True)
            feature_data.append(encoded)
        
        
        temporal_features = self.df[['Month', 'Weekday', 'Hour']]
        feature_data.append(temporal_features)
        
       
        X = pd.concat(feature_data, axis=1)
        y = self.df['Completed']
        
       
        self.feature_columns = X.columns.tolist()
        
        
        self.categorical_values = {
            'service_types': sorted(self.df['Service Request Type'].unique().tolist()),
            'divisions': sorted(self.df['Division'].unique().tolist()),
            'wards': sorted(self.df['Ward'].unique().tolist())
        }
        
        print(f"Feature matrix shape: {X.shape}")
        print(f"Features: {len(self.feature_columns)} total")
        
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )
        
       
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            class_weight='balanced'
        )
        
        self.model.fit(X_train, y_train)
        
        
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)
        
      
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        print(f"   Model Performance:")
        print(f"   Accuracy:  {accuracy:.3f}")
        print(f"   Precision: {precision:.3f}")
        print(f"   Recall:    {recall:.3f}")
        print(f"   F1-Score:  {f1:.3f}")
        
        
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False).head(10)
        
        return {
            "features": feature_importance['feature'].tolist(),
            "importance": [round(imp, 4) for imp in feature_importance['importance'].tolist()]
        }