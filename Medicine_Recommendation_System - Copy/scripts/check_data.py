import joblib
import os

# Path to your medicine.pkl
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
medicine_path = os.path.join(BASE_DIR, 'models', 'medicine.pkl')

try:
    med_data = joblib.load(medicine_path)
    print("--- Medicine Data Check ---")
    print(f"Type of data: {type(med_data)}")
    
    if isinstance(med_data, dict):
        print(f"Total diseases in medicine_dict: {len(med_data)}")
        print("\nSample Data (First 3):")
        for i, (k, v) in enumerate(med_data.items()):
            if i < 3:
                print(f"Disease: '{k}' -> Medicines: {v}")
    else:
        print(f"Data format is not a dictionary. It is: {type(med_data)}")
        print("Preview:", med_data[:5] if hasattr(med_data, '__getitem__') else med_data)
        
except Exception as e:
    print(f"Error reading file: {e}")