import joblib

# Load the dictionary to get the disease names
desc = joblib.load('description.pkl')

# Extract keys (disease names) and sort them alphabetically
disease_names = sorted(list(desc.keys()))

print(f"Total diseases found: {len(disease_names)}")
if len(disease_names) > 15:
    print(f"Disease at index 15 is: '{disease_names[15]}'")