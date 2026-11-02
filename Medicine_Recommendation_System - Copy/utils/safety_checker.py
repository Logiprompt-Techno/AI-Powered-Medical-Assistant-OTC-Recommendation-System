import logging

logger = logging.getLogger(__name__)

# A conservative, evidence-based subset of common OTC medicine interactions and contraindications.
# This acts as the predefined/admin-manageable rules dataset.
SAFETY_RULES = {
    "ibuprofen": {
        "contraindications": ["asthma", "hypertension", "ulcer", "kidney disease", "heart disease"],
        "interactions": ["aspirin", "warfarin", "naproxen", "diclofenac"]
    },
    "paracetamol": {
        "contraindications": ["liver disease", "hepatitis"],
        "interactions": ["warfarin"]
    },
    "acetaminophen": {
        "contraindications": ["liver disease", "hepatitis"],
        "interactions": ["warfarin"]
    },
    "aspirin": {
        "contraindications": ["ulcer", "asthma", "bleeding disorder", "hemophilia"],
        "interactions": ["ibuprofen", "warfarin", "naproxen", "heparin"]
    },
    "naproxen": {
        "contraindications": ["ulcer", "asthma", "heart disease", "kidney disease"],
        "interactions": ["aspirin", "ibuprofen", "warfarin"]
    },
    "cetirizine": {
        "contraindications": ["kidney disease", "liver disease"],
        "interactions": ["alcohol", "sedatives"]
    },
    "loratadine": {
        "contraindications": ["liver disease", "kidney disease"],
        "interactions": ["erythromycin", "cimetidine"]
    },
    "diphenhydramine": {
        "contraindications": ["glaucoma", "asthma", "enlarged prostate"],
        "interactions": ["alcohol", "sedatives", "antidepressants"]
    },
    "omeprazole": {
        "contraindications": ["liver disease"],
        "interactions": ["clopidogrel", "warfarin", "diazepam", "digoxin"]
    },
    "antacids": {
        "contraindications": ["kidney disease"],
        "interactions": ["tetracycline", "ciprofloxacin", "levothyroxine"]
    }
}

def check_medicine_safety(user_profile, recommended_medicines):
    \"\"\"
    Cross-references recommended medicines against the user's safety profile (allergies, conditions, current meds).
    Returns a dictionary with 'warnings', 'safe_checks', and 'unknowns'.
    \"\"\"
    warnings = []
    safe_checks = []
    unknowns = []

    # Normalize user profile data
    user_allergies = [a.strip().lower() for a in user_profile.get('allergies', '').split(',') if a.strip()]
    user_conditions = [c.strip().lower() for c in user_profile.get('medical_conditions', '').split(',') if c.strip()]
    user_meds = [m.strip().lower() for m in user_profile.get('current_medicines', '').split(',') if m.strip()]

    # If the user has absolutely no profile data, we can't do a personal safety check.
    if not user_allergies and not user_conditions and not user_meds:
        return {
            "warnings": [],
            "safe_checks": [],
            "unknowns": [],
            "message": "No medical safety profile found. Please update your profile for personalized safety checks."
        }

    for rec_med_raw in recommended_medicines:
        rec_med = rec_med_raw.strip().lower()
        conflict_found = False

        # 1. Direct Allergy Check
        for allergy in user_allergies:
            if allergy in rec_med or rec_med in allergy:
                warnings.append(f"⚠️ Allergy Alert: You reported an allergy to '{allergy}', which conflicts with '{rec_med_raw}'.")
                conflict_found = True

        # 2. Rule-based checks (Conditions & Interactions)
        rule_matched = False
        for rule_med, rules in SAFETY_RULES.items():
            if rule_med in rec_med or rec_med in rule_med:
                rule_matched = True
                
                # Check Contraindications (Existing Conditions)
                for condition in rules.get("contraindications", []):
                    if any(condition in c or c in condition for c in user_conditions):
                        warnings.append(f"⚠️ Contraindication: '{rec_med_raw}' may be unsafe with your condition '{condition}'.")
                        conflict_found = True

                # Check Drug Interactions (Current Medicines)
                for int_med in rules.get("interactions", []):
                    if any(int_med in m or m in int_med for m in user_meds):
                        warnings.append(f"⚠️ Drug Interaction: '{rec_med_raw}' may negatively interact with your current medicine '{int_med}'.")
                        conflict_found = True

        # Determine status for this medicine
        if not rule_matched:
            # We don't have rules for this medicine. Do not assume it's safe.
            unknowns.append(f"Information for '{rec_med_raw}' is unavailable in our safety database.")
        elif not conflict_found:
            # We checked rules and found no conflicts against the user's specific profile
            safe_checks.append(f"No known conflict found for '{rec_med_raw}' based on available rules and your profile.")

    return {
        "warnings": warnings,
        "safe_checks": safe_checks,
        "unknowns": unknowns
    }
