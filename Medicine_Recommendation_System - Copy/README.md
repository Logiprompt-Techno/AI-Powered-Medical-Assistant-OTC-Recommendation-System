# OTC Medicine Recommendation System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-Framework-black)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248)
![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-F7931E)

## 📖 Overview
The **OTC Medicine Recommendation System** is an AI-powered healthcare platform designed to assist users by predicting potential diseases based on their symptoms and providing clinical recommendations for Over-The-Counter (OTC) medicines. It bridges the gap between machine learning diagnostics and practical health tools, featuring an intelligent medicine directory and robust role-based administrative control.

## ✨ Key Features
- **Unified Login System**: A seamless, role-based authentication gateway that intelligently routes Administrators and Normal Users to their respective dashboards while strictly isolating sessions.
- **Disease Prediction Engine**: Utilizes a trained Machine Learning model (Random Forest) to analyze user-inputted symptoms and predict potential diseases with high accuracy.
- **Intelligent Medicine Directory**: A searchable and filterable database of over-the-counter and prescription medicines, complete with clinical uses, dosages, and safety precautions.
- **Personalized User Favorites**: Allows authenticated users to curate and save medicines to their private "My Favorites" dashboard for quick reference.
- **Admin Dashboard**: A secure portal for administrators to manage the medicine database (CRUD operations), monitor global application analytics, and oversee users.

## 🛠️ Tech Stack
- **Backend**: Python (Flask)
- **Database**: MongoDB Atlas
- **Machine Learning**: Scikit-learn (Random Forest Pipeline)
- **Frontend**: HTML5, Vanilla CSS, JavaScript, Jinja2 Templating
- **Security**: Werkzeug password hashing, Server-side session validation

## 🛡️ Security Highlights
- **Role-Based Session Isolation**: Admin and User sessions are strictly decoupled. When an admin logs in, user sessions are purged (and vice versa), eliminating role bleeding.
- **Env-Based Admin Credentials**: Administrator access is controlled exclusively via secure `.env` variables rather than hardcoded database records.
- **Private Data Encryption**: User history and favorites are programmatically locked to the server-side `session.get('user_id')`, preventing tampering via frontend inputs.

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd Medicine_Recommendation_System
```

### 2. Install dependencies
Ensure you have Python installed, then set up your environment:
```bash
# Optional: Create a virtual environment
# python -m venv venv
# source venv/bin/activate (Linux/Mac) or venv\Scripts\activate (Windows)

pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory and configure the following variables:
```env
# Application Security
FLASK_SECRET_KEY=your_super_secret_flask_key

# Database Connection
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.../

# Admin Portal Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_admin_password
```

### 4. Run the Application
Start the Flask server locally:
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your browser to access the platform.
