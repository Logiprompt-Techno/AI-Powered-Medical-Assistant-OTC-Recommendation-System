import os
import sys
import traceback
from flask import Flask, session
import app as myapp
from bson.objectid import ObjectId

with myapp.app.test_client() as c:
    # First, let's find a valid prediction to test with
    pred = myapp.prediction_history.find_one({"user_id": {"$exists": True}})
    if not pred:
        print("No predictions with user_id in DB to test.")
        sys.exit(0)
    
    with c.session_transaction() as sess:
        sess['user_id'] = pred['user_id']
        
    url = f"/user/history/download/{str(pred['_id'])}"
    print(f"Testing URL: {url}")
    
    try:
        response = c.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 500:
            print("Response Data:", response.data.decode())
    except Exception as e:
        print("EXCEPTION RAISED:")
        traceback.print_exc()
