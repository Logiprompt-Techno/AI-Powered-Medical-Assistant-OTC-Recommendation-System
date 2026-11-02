import os
import sys
import traceback
from pymongo import MongoClient
from bson.objectid import ObjectId
import utils.pdf_generator as pdf_gen

MONGO_URI = "mongodb+srv://abhinavsaju1_db_user:abhinav12345@cluster0.4jzdhan.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client.get_database("medicine_recommendation_db")

# Find any valid prediction
pred = db.prediction_history.find_one()
if not pred:
    print("No predictions in DB to test.")
    sys.exit(0)

user = db.users.find_one({"_id": ObjectId(pred['user_id'])})
if not user:
    print("User not found for this prediction.")
    sys.exit(0)

print(f"Testing PDF generation for prediction {pred['_id']}")
try:
    pdf_gen.generate_prediction_pdf(user, pred)
    print("SUCCESS: PDF generated locally without exception.")
except Exception as e:
    print("EXCEPTION OCCURRED IN PDF_GENERATOR:")
    traceback.print_exc()
