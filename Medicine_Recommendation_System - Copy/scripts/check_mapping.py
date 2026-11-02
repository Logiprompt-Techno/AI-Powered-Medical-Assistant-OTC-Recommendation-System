import joblib
import os

print("--- Available PKL Files ---")
print([f for f in os.listdir() if f.endswith('.pkl')])

le = joblib.load('label_encoder.pkl')
print("\n--- Checking Label Encoder ---")
print("Type:", type(le))

if hasattr(le, 'classes_'):
    print("First 5 Classes:", le.classes_[:5])
    if len(le.classes_) > 15:
        print("Disease at index 15:", le.classes_[15])
elif isinstance(le, dict):
    print("It's a dictionary! First few items:", list(le.items())[:5])
else:
    print("Content:", le)