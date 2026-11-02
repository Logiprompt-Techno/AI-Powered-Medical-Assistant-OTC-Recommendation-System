from bson.objectid import ObjectId
import utils.pdf_generator as pdf_gen
from datetime import datetime

user = {'full_name': 'Test User', 'age': 30, 'gender': 'Male', 'height': None, 'weight': None}
pred = {'selected_symptoms': ['fever', 'cough'], 'predicted_disease': 'Flu', 'medicines': ['Paracetamol'], 'precautions': ['Rest'], 'timestamp': datetime.now()}

try:
    pdf_gen.generate_prediction_pdf(user, pred)
    print('SUCCESS')
except Exception as e:
    import traceback
    traceback.print_exc()
