import os, json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from bson.objectid import ObjectId
from .auth import login_required

# Create the admin blueprint
admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin', url_prefix='/admin')


@admin_bp.route('/', strict_slashes=False)
def admin_home():
    return redirect(url_for('login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    from app import prediction_history, db
    
    # 1. Total Predictions
    total_predictions = prediction_history.count_documents({})
    
    # 2. Most Predicted Diseases (Aggregation) - Expanding limit for the chart
    pipeline = [
        {"$group": {"_id": "$predicted_disease", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_diseases = list(prediction_history.aggregate(pipeline))
    
    # 3. Recent 10 Predictions
    recent_predictions = list(prediction_history.find().sort('_id', -1).limit(10))
    
    # 4. Total Users
    total_users = db.users.count_documents({})
    
    # 5. User List with Search
    user_search = request.args.get('user_search')
    user_query = {}
    if user_search:
        user_query = {
            "$or": [
                {"full_name": {"$regex": user_search, "$options": "i"}},
                {"email": {"$regex": user_search, "$options": "i"}}
            ]
        }
    
    user_list = list(db.users.find(user_query, {"password": 0}).sort('_id', -1).limit(50))
    
    # 6. User Feedback
    feedback_list = list(db.feedback.find().sort('created_at', -1).limit(50))
    
    return render_template('admin/dashboard.html', 
                           total_predictions=total_predictions,
                           top_diseases=top_diseases,
                           chart_data=json.dumps(top_diseases),
                           recent_predictions=recent_predictions,
                           total_users=total_users,
                           user_list=user_list,
                           user_search=user_search,
                           feedback_list=feedback_list)

@admin_bp.route('/delete_user/<user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    from app import db, prediction_history
    try:
        # 1. Delete the user document
        db.users.delete_one({"_id": ObjectId(user_id)})
        
        # 2. Delete associated prediction history (stored as string)
        prediction_history.delete_many({"user_id": str(user_id)})
        
        # 3. Delete associated feedback (stored as string)
        db.feedback.delete_many({"user_id": str(user_id)})
        
    except Exception as e:
        print(f"Error deleting user: {e}")
        
    return redirect(url_for('admin.dashboard'))

# ==========================================
# PHASE 9.5: MEDICINE MANAGEMENT
# ==========================================

@admin_bp.route('/medicines')
@login_required
def medicines():
    from app import db
    search = request.args.get('search')
    query = {}
    if search:
        query = {
            "$or": [
                {"name": {"$regex": search, "$options": "i"}},
                {"category": {"$regex": search, "$options": "i"}}
            ]
        }
    medicines_list = list(db.medicines.find(query).sort('_id', -1))
    return render_template('admin/medicines.html', medicines=medicines_list, search=search)

@admin_bp.route('/add_medicine', methods=['POST'])
@login_required
def add_medicine():
    from app import db
    try:
        name = request.form.get('name')
        category = request.form.get('category')
        description = request.form.get('description')
        dosage = request.form.get('dosage')
        side_effects = request.form.get('side_effects')
        is_otc = True if request.form.get('is_otc') == 'yes' else False
        
        if name and category:
            db.medicines.insert_one({
                "name": name,
                "category": category,
                "description": description,
                "dosage": dosage,
                "side_effects": side_effects,
                "disease_category": category,
                "is_otc": is_otc
            })
            flash("Medicine added successfully!", "success")
        else:
            flash("Name and Category are required.", "error")
    except Exception as e:
        flash(f"Error adding medicine: {e}", "error")
        
    return redirect(url_for('admin.medicines'))

@admin_bp.route('/edit_medicine/<medicine_id>', methods=['GET', 'POST'])
@login_required
def edit_medicine(medicine_id):
    from app import db
    try:
        medicine = db.medicines.find_one({"_id": ObjectId(medicine_id)})
        if not medicine:
            flash("Medicine not found.", "error")
            return redirect(url_for('admin.medicines'))
            
        if request.method == 'POST':
            name = request.form.get('name')
            category = request.form.get('category')
            description = request.form.get('description')
            dosage = request.form.get('dosage')
            side_effects = request.form.get('side_effects')
            is_otc = True if request.form.get('is_otc') == 'yes' else False
            
            if name and category:
                db.medicines.update_one(
                    {"_id": ObjectId(medicine_id)},
                    {"$set": {
                        "name": name,
                        "category": category,
                        "description": description,
                        "dosage": dosage,
                        "side_effects": side_effects,
                        "disease_category": category,
                        "is_otc": is_otc
                    }}
                )
                flash("Medicine updated successfully!", "success")
                return redirect(url_for('admin.medicines'))
            else:
                flash("Name and Category are required.", "error")
                
        return render_template('admin/edit_medicine.html', medicine=medicine)
    except Exception as e:
        flash(f"Error editing medicine: {e}", "error")
        return redirect(url_for('admin.medicines'))

@admin_bp.route('/delete_medicine/<medicine_id>', methods=['POST'])
@login_required
def delete_medicine(medicine_id):
    from app import db
    try:
        db.medicines.delete_one({"_id": ObjectId(medicine_id)})
        flash("Medicine deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting medicine: {e}", "error")
        
    return redirect(url_for('admin.medicines'))

# ==========================================
# PHASE 9.6: DISEASE MANAGEMENT
# ==========================================

@admin_bp.route('/diseases')
@login_required
def diseases():
    from app import db
    search = request.args.get('search')
    query = {}
    if search:
        query = {
            "$or": [
                {"name": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}}
            ]
        }
    diseases_list = list(db.diseases.find(query).sort('_id', -1))
    return render_template('admin/diseases.html', diseases=diseases_list, search=search)

@admin_bp.route('/add_disease', methods=['POST'])
@login_required
def add_disease():
    from app import db
    try:
        name = request.form.get('name')
        description = request.form.get('description')
        precautions_raw = request.form.get('precautions', '')
        
        precautions = [p.strip() for p in precautions_raw.split(',') if p.strip()]
        
        if name and description:
            db.diseases.insert_one({
                "name": name,
                "description": description,
                "precautions": precautions
            })
            flash("Disease added successfully!", "success")
        else:
            flash("Name and Description are required.", "error")
    except Exception as e:
        flash(f"Error adding disease: {e}", "error")
        
    return redirect(url_for('admin.diseases'))

@admin_bp.route('/edit_disease/<disease_id>', methods=['GET', 'POST'])
@login_required
def edit_disease(disease_id):
    from app import db
    try:
        disease = db.diseases.find_one({"_id": ObjectId(disease_id)})
        if not disease:
            flash("Disease not found.", "error")
            return redirect(url_for('admin.diseases'))
            
        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            precautions_raw = request.form.get('precautions', '')
            
            precautions = [p.strip() for p in precautions_raw.split(',') if p.strip()]
            
            if name and description:
                db.diseases.update_one(
                    {"_id": ObjectId(disease_id)},
                    {"$set": {
                        "name": name,
                        "description": description,
                        "precautions": precautions
                    }}
                )
                flash("Disease updated successfully!", "success")
                return redirect(url_for('admin.diseases'))
            else:
                flash("Name and Description are required.", "error")
                
        return render_template('admin/edit_disease.html', disease=disease)
    except Exception as e:
        flash(f"Error editing disease: {e}", "error")
        return redirect(url_for('admin.diseases'))

@admin_bp.route('/delete_disease/<disease_id>', methods=['POST'])
@login_required
def delete_disease(disease_id):
    from app import db
    try:
        db.diseases.delete_one({"_id": ObjectId(disease_id)})
        flash("Disease deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting disease: {e}", "error")
        
    return redirect(url_for('admin.diseases'))



