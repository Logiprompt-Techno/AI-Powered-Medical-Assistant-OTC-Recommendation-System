import os
import sys
import traceback
from flask import Flask, session
import app as myapp
from bson.objectid import ObjectId

with myapp.app.test_client() as c:
    # Test ALL predictions in DB
    preds = list(myapp.prediction_history.find({"user_id": {"$exists": True}}))
    print(f"Found {len(preds)} predictions in DB.")
    
    for pred in preds:
        with c.session_transaction() as sess:
            sess['user_id'] = pred['user_id']
            
        url = f"/user/history/download/{str(pred['_id'])}"
        print(f"Testing URL: {url}")
        
        try:
            response = c.get(url)
            if response.status_code == 500:
                print(f"FAILED for {url}! Response Data: {response.data.decode()}")
                
                # Let's try running it manually to get the exact traceback
                import utils.pdf_generator as pdf_gen
                user = myapp.db.users.find_one({'_id': ObjectId(pred['user_id'])})
                try:
                    pdf_gen.generate_prediction_pdf(user, pred)
                except Exception as e:
                    print("EXACT TRACEBACK:")
                    traceback.print_exc()
            else:
                print(f"Success for {url} (Status: {response.status_code})")
        except Exception as e:
            print("EXCEPTION RAISED:")
            traceback.print_exc()
