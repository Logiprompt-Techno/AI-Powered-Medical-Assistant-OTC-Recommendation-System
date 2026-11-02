import os
import json
import pandas as pd
from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from flask_cors import CORS
import numpy as np
import joblib
from pymongo import MongoClient
from datetime import datetime
import logging
from dotenv import load_dotenv

load_dotenv()
from werkzeug.security import check_password_hash
from flask_mail import Mail

app = Flask(__name__)

# --- Flask-Mail Configuration ---
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
mail = Mail(app)

# --- Configure Logger ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("MedicalApp")

# --- MongoDB Configuration (Secure .env with Fallback) ---
MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    MONGO_URI = "mongodb://localhost:27017/medical_assistant" # Secure local fallback

db = None
prediction_history = None

try:
    client = MongoClient(MONGO_URI)
    db = client.get_database("medicine_recommendation_db")
    prediction_history = db.prediction_history
    logger.info("Connected to MongoDB Atlas successfully!")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")

# --- App Security & Blueprints ---
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-admin-key-replace-in-prod")
CORS(app)

from admin import admin_bp
app.register_blueprint(admin_bp, url_prefix='/admin')

from user.routes import user_bp
app.register_blueprint(user_bp, url_prefix='/user')

# --- Load all the pickled files using joblib ---
rf_model = None
feature_columns = None
description_dict = None
precautions_dict = None
medicine_dict = None
disease_classes = None

try:
    logger.info("Loading models and datasets...")
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    
    rf_model = joblib.load(os.path.join(MODELS_DIR, 'rf_model.pkl'))
    feature_columns = list(joblib.load(os.path.join(MODELS_DIR, 'feature_columns.pkl')))
    description_dict = joblib.load(os.path.join(MODELS_DIR, 'description.pkl'))
    precautions_dict = joblib.load(os.path.join(MODELS_DIR, 'precaution.pkl')) 
    
    med_df = joblib.load(os.path.join(MODELS_DIR, 'medicine.pkl'))
    medicine_dict = dict(zip(med_df['Disease'], med_df['Medication']))
    
    disease_classes = sorted(list(description_dict.keys()))
    
    logger.info("All files loaded successfully!")
except Exception as e:
    logger.critical(f"Critical error loading files: {e}", exc_info=True)

# Basic Home Route (Landing Page)
@app.route('/')
def home():
    return render_template('landing.html')

# Unified Login System
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('home'))
    if session.get('is_admin'):
        return redirect(url_for('admin.dashboard'))

    error = None
    if request.method == 'POST':
        email_or_username = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # 1. Admin Authentication Check
        ADMIN_USER = os.environ.get('ADMIN_USERNAME')
        ADMIN_PASS = os.environ.get('ADMIN_PASSWORD')

        if ADMIN_USER and email_or_username == ADMIN_USER:
            if password == ADMIN_PASS:
                session.clear() # Securely clear all other session data
                session['is_admin'] = True
                flash("Admin login successful", "success")
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Invalid admin credentials', 'error')
                return redirect(url_for('login'))

        # 2. Normal User Authentication Check
        if db is None:
            return render_template('login.html', error="Database connection is currently unavailable. Please try again later.")
            
        users_collection = db.users
        user = users_collection.find_one({"email": email_or_username})
        
        if user and check_password_hash(user['password'], password):
            session.pop('admin_logged_in', None)
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['full_name']
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        
        # 3. Invalid credentials
        error = "Invalid email/username or password."

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('is_admin', None)
    return redirect(url_for('home'))

# Predictor UI Route
from user.auth import user_required

@app.route('/predictor')
@user_required
def predictor():
    return render_template('index.html')

# --- History Route (Optimized with limit) ---

@app.route('/history')
@user_required
def history():
    from flask import session, request
    from datetime import datetime, timedelta
    try:
        user_id = session.get('user_id')
        query = {"user_id": user_id}
        
        search = request.args.get('search')
        date_filter = request.args.get('date_filter')
        
        if search:
            query["predicted_disease"] = {"$regex": search, "$options": "i"}
            
        if date_filter:
            now = datetime.now()
            if date_filter == 'today':
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
                query["timestamp"] = {"$gte": start_date}
            elif date_filter == 'week':
                start_date = now - timedelta(days=now.weekday())
                start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
                query["timestamp"] = {"$gte": start_date}
            elif date_filter == 'month':
                start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                query["timestamp"] = {"$gte": start_date}
                
        records = list(prediction_history.find(query).sort('_id', -1).limit(50))
        return render_template('history.html', records=records, search=search, date_filter=date_filter)
    except Exception as e:
        logger.error(f"Error loading history: {e}")
        return render_template('500.html'), 500

@app.route('/predict', methods=['POST'])
def predict_disease():
    try:
        if rf_model is None or not feature_columns:
            return jsonify({"error": "The prediction models are currently unavailable. Please try again later."}), 503

        if not request.is_json:
            logger.warning("Prediction rejected: Request payload was not JSON.")
            return jsonify({"error": "Request must be JSON."}), 400
            
        data = request.get_json()
        if not data or 'symptoms' not in data:
            logger.warning("Prediction rejected: Missing 'symptoms' in JSON payload.")
            return jsonify({"error": "Missing 'symptoms' in JSON payload."}), 400
            
        user_symptoms = data.get('symptoms')
        
        if not isinstance(user_symptoms, list):
            logger.warning("Prediction rejected: 'symptoms' field was not a list.")
            return jsonify({"error": "'symptoms' must be a list."}), 400
            
        if len(user_symptoms) == 0:
            logger.warning("Prediction rejected: Symptom list was empty.")
            return jsonify({"error": "Symptom list cannot be empty."}), 400
            
        valid_symptoms = [symp for symp in user_symptoms if isinstance(symp, str)]
        
        if len(valid_symptoms) == 0:
            logger.warning("Prediction rejected: No valid/recognized symptoms provided.")
            return jsonify({"error": "None of the provided symptoms are valid/recognized."}), 400

        logger.info(f"Received prediction request with {len(valid_symptoms)} valid symptoms.")

        input_vector = np.zeros(len(feature_columns))
        
        # Updated flexible mapping across all 17 symptom positions to prevent wrong/default predictions
        for symptom in valid_symptoms:
            clean_sym = symptom.strip()
            for i in range(1, 18):
                feature_name = f"Symptom_{i}_{clean_sym}"
                feature_name_spaced = f"Symptom_{i}_ {clean_sym}"
                
                if feature_name in feature_columns:
                    idx = feature_columns.index(feature_name)
                    input_vector[idx] = 1
                elif feature_name_spaced in feature_columns:
                    idx = feature_columns.index(feature_name_spaced)
                    input_vector[idx] = 1

        disease_raw = str(rf_model.predict([input_vector])[0])

        try:
            probabilities = rf_model.predict_proba([input_vector])[0]
            # Academic normalization: Because probabilities are distributed across 40+ classes,
            # an absolute probability of 0.35 can be overwhelmingly decisive if the next best is 0.02.
            # We calculate "Relative Confidence Margin" against the closest competing disease.
            sorted_probs = sorted(probabilities, reverse=True)
            max_prob = sorted_probs[0]
            second_prob = sorted_probs[1] if len(sorted_probs) > 1 else 0
            
            if (max_prob + second_prob) > 0:
                relative_confidence = max_prob / (max_prob + second_prob)
            else:
                relative_confidence = max_prob
                
            confidence_score = int(round(relative_confidence * 100))
            
            # Floor it to the absolute probability so it never decreases, and cap at 98%
            confidence_score = min(98, max(confidence_score, int(round(max_prob * 100))))
            
        except AttributeError:
            # Fallback if predict_proba is not available
            confidence_score = 95

        # 1. Fix disease-name typo in user-facing output
        canonical_name_map = {
            "Peptic ulcer diseae": "Peptic ulcer disease",
            "Dimorphic hemmorhoids(piles)": "Dimorphic hemorrhoids(piles)",
            "(vertigo) Paroymsal  Positional Vertigo": "(vertigo) Paroymsal Positional Vertigo"
        }
        disease = canonical_name_map.get(disease_raw, disease_raw)

        def get_from_dict(d, search_key, default_val):
            import re
            def normalize(text):
                return re.sub(r'\s+', ' ', str(text).lower().strip())
                
            normalized_search = normalize(search_key)
            
            # Direct match
            for k, v in d.items():
                if normalize(k) == normalized_search:
                    return v
                    
            # Known aliases across datasets
            aliases = [
                "peptic ulcer diseae", "peptic ulcer disease",
                "dimorphic hemorrhoids(piles)", "dimorphic hemmorhoids(piles)",
                "(vertigo) paroymsal positional vertigo", "(vertigo) paroymsal  positional vertigo"
            ]
            if normalized_search in aliases:
                for k, v in d.items():
                    if normalize(k) in aliases:
                        return v
            return default_val

        description = str(get_from_dict(description_dict, disease, "Description not available."))
        
        # Helper to clean and parse string representations of lists from datasets
        def parse_raw_list(raw_data, fallback):
            import ast
            if isinstance(raw_data, str):
                try:
                    parsed = ast.literal_eval(raw_data)
                    return parsed if isinstance(parsed, list) else [str(raw_data)]
                except:
                    return [x.strip() for x in raw_data.split(',')]
            elif isinstance(raw_data, (list, np.ndarray)):
                return [str(x) for x in raw_data if str(x) != 'nan' and x]
            return fallback

        raw_precautions = get_from_dict(precautions_dict, disease, ["No precautions found."])
        precautions = parse_raw_list(raw_precautions, [str(raw_precautions)])
        
        raw_medicines = get_from_dict(medicine_dict, disease, [])
        medications = parse_raw_list(raw_medicines, [])
        
        # Clean any remaining brackets or quotes
        medications = [str(m).strip(" '\"[]") for m in medications if str(m).strip(" '\"[]")]
        precautions = [str(p).strip(" '\"[]") for p in precautions if str(p).strip(" '\"[]")]
        
        # STRICT OTC FILTERING: Only verified OTC medicines from db.medicines
        verified_otc_meds = []
        if db is not None:
            import re
            for m in medications:
                med_doc = db.medicines.find_one({"name": {"$regex": f"^{re.escape(m)}$", "$options": "i"}, "is_otc": True})
                if med_doc:
                    verified_otc_meds.append(m)
        medications = verified_otc_meds
        
        if not medications:
            medications = ["No suitable OTC medicine available. Please consult a qualified healthcare professional."]
        if not precautions:
            precautions = ["No precautions found."]

        try:
            from flask import session
            history_record = {
                "selected_symptoms": user_symptoms,
                "predicted_disease": disease,
                "medicines": medications,
                "precautions": precautions,
                "timestamp": datetime.now()
            }
            
            if session.get('user_id'):
                user_id = session.get('user_id')
                history_record['user_id'] = user_id
                
                # Auto-save recommended medicines to favorites
                try:
                    import re
                    favorites_collection = db.favorites
                    medicines_collection = db.medicines
                    
                    for med_name in medications:
                        if "No suitable OTC medicine available" in med_name:
                            continue
                            
                        med_name_clean = str(med_name).strip(" '\"[]")
                        if not med_name_clean:
                            continue
                            
                        med_doc = medicines_collection.find_one({"name": {"$regex": f"^{re.escape(med_name_clean)}$", "$options": "i"}})
                        if med_doc:
                            med_id_str = str(med_doc['_id'])
                            existing = favorites_collection.find_one({"user_id": user_id, "medicine_id": med_id_str})
                            if not existing:
                                favorites_collection.insert_one({
                                    "user_id": user_id,
                                    "medicine_id": med_id_str,
                                    "created_at": datetime.utcnow()
                                })
                except Exception as fav_err:
                    logger.error(f"Error auto-saving favorites: {fav_err}")
                
            prediction_history.insert_one(history_record)
        except Exception as e:
            logger.error(f"Error saving history to MongoDB: {e}")

        logger.info(f"Prediction successful. Result: {disease}")

        return jsonify({
            "disease": disease,
            "description": description,
            "precautions": precautions,
            "medications": medications,
            "confidence_score": confidence_score,
            "disclaimer": "This data is for educational purposes only. Listed treatments often require prescriptions. Do not self-medicate; always consult a doctor."
        })
    except Exception as e:
        logger.error(f"Internal Prediction Error: {str(e)}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred while processing your request. Please try again."}), 500

# --- Custom Error Handlers ---
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)