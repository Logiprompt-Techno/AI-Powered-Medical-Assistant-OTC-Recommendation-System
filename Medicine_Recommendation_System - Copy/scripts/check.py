import joblib
import pandas as pd

# Description file load cheyyunnu
desc = joblib.load('description.pkl')
print("Data Type:", type(desc))

if isinstance(desc, pd.DataFrame):
    print("Columns in DataFrame:", desc.columns.tolist())
elif isinstance(desc, dict):
    print("First few keys in Dictionary:", list(desc.keys())[:3])
else:
    print("Other Type:", desc)