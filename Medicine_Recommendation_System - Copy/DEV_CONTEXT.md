# Project Development Context

## Overview
This project is an **OTC Medicine Recommendation System** built with **Flask** and **MongoDB Atlas**. It integrates a **Random Forest disease prediction model** to analyze symptoms and provide clinical recommendations. 

## Authentication Architecture
The system uses a **Unified Role-Based Login System** (`/login`):
- **Admins** authenticate using credentials defined in `.env` variables (`ADMIN_USERNAME`, `ADMIN_PASSWORD`).
- **Normal Users** authenticate via standard registration/login against the MongoDB `users` collection using Werkzeug password hashing.

## Session Management & Isolation
To prevent role-bleeding and unauthorized access, strict server-side session isolation is enforced:
- Normal user sessions are tracked via `session['user_id']`.
- Admin sessions are tracked via `session['admin_logged_in']`.
- **Session Purging:** When an admin logs in, any existing `user_id` session is explicitly cleared. Conversely, when a user logs in, any `admin_logged_in` session is cleared. This guarantees strict boundary enforcement.

## Machine Learning Integration
- **Model:** Random Forest (`model.pkl`) trained on clinical symptom datasets.
- **Endpoint:** `/predict` route handles symptom ingestion, model inference, and output mapping without interfering with core user data logic.

## Key Developer Rules
- **Do not modify** the prediction logic (`/predict`) or the serialized ML models.
- **Do not introduce** frontend dependencies for user validation (e.g., passing `user_id` in hidden forms); always rely on Flask's secure server-side `session`.
- **Routing:** All old fragmented login paths (`/admin/login`, `/user/login`) have been removed and replaced by the unified `/login` flow. Maintain this architecture for all future authentication updates.
