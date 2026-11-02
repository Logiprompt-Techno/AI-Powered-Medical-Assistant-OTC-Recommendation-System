import os
import re
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, jsonify
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from .auth import user_required

user_bp = Blueprint('user', __name__, template_folder='../templates/user', url_prefix='/user')


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('user.dashboard'))
        
    error = None
    if request.method == 'POST':
        from app import db
        if db is None:
            return render_template('user/register.html', error="Database connection is currently unavailable. Please try again later.")
        users_collection = db.users
        
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        age = request.form.get('age')
        gender = request.form.get('gender')
        height = request.form.get('height')
        weight = request.form.get('weight')
        
        if not all([full_name, email, password, age, gender]):
            error = "Please fill in all required fields."
        elif not re.match(r'^[A-Za-z\s]+$', full_name) or len(full_name) < 3:
            error = "Full Name must be at least 3 characters and contain only letters and spaces."
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            error = "Please enter a valid email address."
        elif len(password) < 6:
            error = "Password must be at least 6 characters long."
        elif gender not in ['Male', 'Female', 'Other']:
            error = "Please select a valid gender."
        else:
            try:
                age_val = int(age)
                if age_val < 0 or age_val > 120:
                    error = "Age must be between 0 and 120."
            except ValueError:
                error = "Age must be a valid number."
                
            if not error and height:
                try:
                    h_val = float(height)
                    if h_val < 0:
                        error = "Height cannot be negative."
                except ValueError:
                    error = "Height must be a valid number."
                    
            if not error and weight:
                try:
                    w_val = float(weight)
                    if w_val < 0:
                        error = "Weight cannot be negative."
                except ValueError:
                    error = "Weight must be a valid number."
                    
        if not error and users_collection.find_one({"email": email}):
            error = "Email address already registered."
            
        if not error:
            try:
                hashed_password = generate_password_hash(password)
                new_user = {
                    "full_name": full_name,
                    "email": email,
                    "password": hashed_password,
                    "age": int(age) if age else None,
                    "gender": gender,
                    "height": float(height) if height else None,
                    "weight": float(weight) if weight else None
                }
                result = users_collection.insert_one(new_user)
                # Redirect to login page after successful registration
                return redirect(url_for('login'))
            except Exception as e:
                error = f"An error occurred: {str(e)}"
                
    return render_template('user/register.html', error=error)

@user_bp.route('/dashboard')
@user_required
def dashboard():
    from app import prediction_history
    # Get user's recent predictions and total count
    user_id = session.get('user_id')
    recent_predictions = list(prediction_history.find({"user_id": user_id}).sort('_id', -1).limit(5))
    total_predictions = prediction_history.count_documents({"user_id": user_id})
    return render_template('user/dashboard.html', recent_predictions=recent_predictions, total_predictions=total_predictions)

@user_bp.route('/profile', methods=['GET', 'POST'])
@user_required
def profile():
    from app import db
    users_collection = db.users
    user_id = session.get('user_id')
    
    error = None
    success = None
    
    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        height = request.form.get('height')
        weight = request.form.get('weight')
        allergies = request.form.get('allergies', '')
        medical_conditions = request.form.get('medical_conditions', '')
        current_medicines = request.form.get('current_medicines', '')
        
        try:
            update_data = {
                "age": int(age) if age else None,
                "gender": gender,
                "height": float(height) if height else None,
                "weight": float(weight) if weight else None,
                "allergies": allergies,
                "medical_conditions": medical_conditions,
                "current_medicines": current_medicines
            }
            users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
            success = "Profile updated successfully."
        except Exception as e:
            error = f"Error updating profile: {str(e)}"
            
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    return render_template('user/profile.html', user=user, error=error, success=success)

@user_bp.route('/feedback', methods=['POST'])
@user_required
def submit_feedback():
    try:
        from app import db
        feedback_collection = db.feedback
        
        data = request.get_json()
        rating = data.get('rating')
        message = data.get('comments') or data.get('message') or ""
        
        if not rating:
            return jsonify({"status": "error", "message": "Rating is required."}), 400
            
        feedback_entry = {
            "user_id": session.get('user_id'),
            "user_name": session.get('user_name'),
            "rating": int(rating),
            "message": str(message),
            "created_at": datetime.now()
        }
        
        feedback_collection.insert_one(feedback_entry)
        return jsonify({"status": "success", "message": "Thank you for your feedback!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@user_bp.route('/tools')
@user_required
def tools():
    return render_template('user/tools.html')

@user_bp.route('/medicines', methods=['GET'])
@user_required
def medicines():
    from app import db
    medicines_collection = db.medicines
    favorites_collection = db.favorites
    
    search_query = request.args.get('search', '').strip()
    query = {}
    if search_query:
        query = {
            '$or': [
                {'name': {'$regex': search_query, '$options': 'i'}},
                {'disease_category': {'$regex': search_query, '$options': 'i'}}
            ]
        }
        
    medicines_list = list(medicines_collection.find(query))
    
    # Get user's saved medicine IDs to display the correct button state
    user_id = session.get('user_id')
    user_favorites = list(favorites_collection.find({"user_id": user_id}))
    saved_medicine_ids = [fav['medicine_id'] for fav in user_favorites]
    
    return render_template('user/medicines.html', medicines=medicines_list, search_query=search_query, saved_medicine_ids=saved_medicine_ids)

@user_bp.route('/favorites/toggle/<medicine_id>', methods=['POST'])
@user_required
def toggle_favorite(medicine_id):
    from app import db
    favorites_collection = db.favorites
    user_id = session.get('user_id')
    
    existing_favorite = favorites_collection.find_one({"user_id": user_id, "medicine_id": medicine_id})
    
    if existing_favorite:
        # Remove from favorites
        favorites_collection.delete_one({"_id": existing_favorite['_id']})
        return jsonify({"status": "removed"})
    else:
        # Add to favorites
        favorites_collection.insert_one({
            "user_id": user_id,
            "medicine_id": medicine_id,
            "created_at": datetime.utcnow()
        })
        return jsonify({"status": "added"})

@user_bp.route('/favorites', methods=['GET'])
@user_required
def favorites():
    from app import db
    favorites_collection = db.favorites
    medicines_collection = db.medicines
    
    user_id = session.get('user_id')
    
    # Get user's saved medicine IDs
    user_favorites = list(favorites_collection.find({"user_id": user_id}).sort("created_at", -1))
    saved_medicine_ids = [ObjectId(fav['medicine_id']) for fav in user_favorites]
    
    # Fetch actual medicine documents
    if saved_medicine_ids:
        # We need to preserve the sorting order of saved medicines based on created_at
        # An easy way is to fetch all and then sort in python, or since it's a small list, it's fine.
        medicines_cursor = medicines_collection.find({"_id": {"$in": saved_medicine_ids}})
        med_dict = {str(med['_id']): med for med in medicines_cursor}
        saved_medicines = [med_dict[fav['medicine_id']] for fav in user_favorites if fav['medicine_id'] in med_dict]
    else:
        saved_medicines = []
        
    # All displayed medicines in this view are saved
    return render_template('user/favorites.html', medicines=saved_medicines, saved_medicine_ids=[fav['medicine_id'] for fav in user_favorites])



@user_bp.route('/history/download/<prediction_id>', methods=['GET'])
@user_required
def download_pdf(prediction_id):
    from app import db, prediction_history
    from flask import send_file
    import utils.pdf_generator as pdf_gen

    try:
        user_id = session.get('user_id')
        # Fetch Prediction
        prediction = prediction_history.find_one({'_id': ObjectId(prediction_id), 'user_id': user_id})
        if not prediction:
            return jsonify({'error': 'Prediction not found or access denied.'}), 404

        # Fetch User
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'error': 'User not found.'}), 404

        # Generate PDF
        pdf_buffer = pdf_gen.generate_prediction_pdf(user, prediction)
        
        # Formulate filename
        raw_timestamp = prediction.get('timestamp')
        report_date = raw_timestamp if raw_timestamp else datetime.now()
        date_str = report_date.strftime('%Y-%m-%d')
        filename = f"Medical_Report_{date_str}.pdf"

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        import traceback
        error_tb = traceback.format_exc()
        current_app.logger.error(f"Error generating PDF:\n{error_tb}")
        print("EXACT PDF ERROR:", error_tb)
        return jsonify({'error': 'Internal server error while generating PDF.', 'details': str(e)}), 500

@user_bp.route('/history/email/<prediction_id>', methods=['POST'])
def email_pdf(prediction_id):
    from app import db, prediction_history, mail
    from flask_mail import Message
    import utils.pdf_generator as pdf_gen
    from datetime import datetime
    
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': 'Your session has expired. Please log in again to send emails.'}), 401
        
        # Fetch Prediction
        prediction = prediction_history.find_one({'_id': ObjectId(prediction_id), 'user_id': user_id})
        if not prediction:
            return jsonify({'success': False, 'message': 'Prediction not found or access denied.'}), 404

        # Fetch User
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if not user or not user.get('email'):
            return jsonify({'success': False, 'message': 'User email not found.'}), 404

        # Generate PDF in memory
        pdf_buffer = pdf_gen.generate_prediction_pdf(user, prediction)
        
        raw_timestamp = prediction.get('timestamp')
        report_date = raw_timestamp if raw_timestamp else datetime.now()
        date_str = report_date.strftime('%Y-%m-%d')
        filename = f"Medical_Report_{date_str}.pdf"

        # Construct Email
        msg = Message(
            subject=f"Your AI Medical Report ({date_str})",
            recipients=[user['email']],
            body="Hello,\n\nPlease find attached your AI Medical Report generated from the OTC Medicine Recommendation System.\n\nDisclaimer: This is for informational purposes only. Do not self-medicate.\n\nStay healthy!"
        )
        msg.attach(filename, 'application/pdf', pdf_buffer.read())
        
        # Send Email
        mail.send(msg)
        return jsonify({'success': True, 'message': 'Report emailed successfully!'}), 200

    except Exception as e:
        import traceback
        error_tb = traceback.format_exc()
        current_app.logger.error(f"Error emailing PDF:\n{error_tb}")
        print("EXACT EMAIL ERROR:", error_tb)
        return jsonify({'success': False, 'message': 'Internal server error while sending email.', 'details': str(e)}), 500


@user_bp.route('/safety-check', methods=['POST'])
@user_required
def safety_check():
    from flask import request, jsonify
    from app import db
    from utils.safety_checker import check_medicine_safety
    
    try:
        data = request.get_json()
        if not data or 'medicines' not in data:
            return jsonify({"error": "Missing 'medicines' list."}), 400
            
        medicines = data.get('medicines')
        if not isinstance(medicines, list):
            return jsonify({"error": "'medicines' must be a list."}), 400
            
        user_id = session.get('user_id')
        user = db.users.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            return jsonify({"error": "User not found."}), 404
            
        safety_report = check_medicine_safety(user, medicines)
        return jsonify(safety_report), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if session.get('user_id'):
        return redirect(url_for('user.dashboard'))
        
    if request.method == 'POST':
        from app import db
        from flask import flash
        email = request.form.get('email')
        
        if email:
            user = db.users.find_one({'email': email})
            if user:
                return redirect(url_for('user.reset_password', email=email))
            else:
                flash('If an account with this email exists, a password reset link has been provided.', 'info')
        else:
            flash('Please enter your email address.', 'error')
            
    return render_template('user/forgot_password.html')

@user_bp.route('/reset-password/<email>', methods=['GET', 'POST'])
def reset_password(email):
    if session.get('user_id'):
        return redirect(url_for('user.dashboard'))
        
    from app import db
    from flask import flash
    user = db.users.find_one({'email': email})
    
    if not user:
        flash('Invalid or expired reset attempt.', 'error')
        return redirect(url_for('user.forgot_password'))
        
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not password or len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
        elif password != confirm_password:
            flash('Passwords do not match.', 'error')
        else:
            hashed_password = generate_password_hash(password)
            db.users.update_one(
                {'_id': user['_id']},
                {'$set': {'password': hashed_password}}
            )
            flash('Your password has been successfully reset. You may now login.', 'success')
            return redirect(url_for('login'))
            
    return render_template('user/reset_password.html', email=email)
