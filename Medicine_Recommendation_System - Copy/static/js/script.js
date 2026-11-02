// 1. Complete List of Symptoms from the Dataset (Exact Spelling)
const allSymptoms = [
    { id: "itching", label: "Itching" },
    { id: "skin_rash", label: "Skin Rash" },
    { id: "nodal_skin_eruptions", label: "Nodal Skin Eruptions" },
    { id: "continuous_sneezing", label: "Continuous Sneezing" },
    { id: "shivering", label: "Shivering" },
    { id: "chills", label: "Chills" },
    { id: "joint_pain", label: "Joint Pain" },
    { id: "stomach_pain", label: "Stomach Pain" },
    { id: "acidity", label: "Acidity" },
    { id: "ulcers_on_tongue", label: "Ulcers on Tongue" },
    { id: "muscle_wasting", label: "Muscle Wasting" },
    { id: "vomiting", label: "Vomiting" },
    { id: "burning_micturition", label: "Burning Micturition" },
    { id: "spotting_urination", label: "Spotting Urination" },
    { id: "fatigue", label: "Fatigue" },
    { id: "weight_gain", label: "Weight Gain" },
    { id: "anxiety", label: "Anxiety" },
    { id: "cold_hands_and_feets", label: "Cold Hands and Feets" },
    { id: "mood_swings", label: "Mood Swings" },
    { id: "weight_loss", label: "Weight Loss" },
    { id: "restlessness", label: "Restlessness" },
    { id: "lethargy", label: "Lethargy" },
    { id: "patches_in_throat", label: "Patches in Throat" },
    { id: "irregular_sugar_level", label: "Irregular Sugar Level" },
    { id: "cough", label: "Cough" },
    { id: "high_fever", label: "High Fever" },
    { id: "sunken_eyes", label: "Sunken Eyes" },
    { id: "breathlessness", label: "Breathlessness" },
    { id: "sweating", label: "Sweating" },
    { id: "dehydration", label: "Dehydration" },
    { id: "indigestion", label: "Indigestion" },
    { id: "headache", label: "Headache" },
    { id: "yellowish_skin", label: "Yellowish Skin" },
    { id: "dark_urine", label: "Dark Urine" },
    { id: "nausea", label: "Nausea" },
    { id: "loss_of_appetite", label: "Loss of Appetite" },
    { id: "pain_behind_the_eyes", label: "Pain Behind The Eyes" },
    { id: "back_pain", label: "Back Pain" },
    { id: "constipation", label: "Constipation" },
    { id: "abdominal_pain", label: "Abdominal Pain" },
    { id: "diarrhoea", label: "Diarrhoea" },
    { id: "mild_fever", label: "Mild Fever" },
    { id: "yellow_urine", label: "Yellow Urine" },
    { id: "yellowing_of_eyes", label: "Yellowing Of Eyes" },
    { id: "acute_liver_failure", label: "Acute Liver Failure" },
    { id: "fluid_overload", label: "Fluid Overload" },
    { id: "swelling_of_stomach", label: "Swelling Of Stomach" },
    { id: "swelled_lymph_nodes", label: "Swelled Lymph Nodes" },
    { id: "malaise", label: "Malaise" },
    { id: "blurred_and_distorted_vision", label: "Blurred And Distorted Vision" },
    { id: "phlegm", label: "Phlegm" },
    { id: "throat_irritation", label: "Throat Irritation" },
    { id: "redness_of_eyes", label: "Redness Of Eyes" },
    { id: "sinus_pressure", label: "Sinus Pressure" },
    { id: "runny_nose", label: "Runny Nose" },
    { id: "congestion", label: "Congestion" },
    { id: "chest_pain", label: "Chest Pain" },
    { id: "weakness_in_limbs", label: "Weakness In Limbs" },
    { id: "fast_heart_rate", label: "Fast Heart Rate" },
    { id: "pain_during_bowel_movements", label: "Pain During Bowel Movements" },
    { id: "pain_in_anal_region", label: "Pain In Anal Region" },
    { id: "bloody_stool", label: "Bloody Stool" },
    { id: "irritation_in_anus", label: "Irritation In Anus" },
    { id: "neck_pain", label: "Neck Pain" },
    { id: "dizziness", label: "Dizziness" },
    { id: "cramps", label: "Cramps" },
    { id: "bruising", label: "Bruising" },
    { id: "obesity", label: "Obesity" },
    { id: "swollen_legs", label: "Swollen Legs" },
    { id: "swollen_blood_vessels", label: "Swollen Blood Vessels" },
    { id: "puffy_face_and_eyes", label: "Puffy Face And Eyes" },
    { id: "enlarged_thyroid", label: "Enlarged Thyroid" },
    { id: "brittle_nails", label: "Brittle Nails" },
    { id: "swollen_extremeties", label: "Swollen Extremeties" },
    { id: "excessive_hunger", label: "Excessive Hunger" },
    { id: "extra_marital_contacts", label: "Extra Marital Contacts" },
    { id: "drying_and_tingling_lips", label: "Drying And Tingling Lips" },
    { id: "slurred_speech", label: "Slurred Speech" },
    { id: "knee_pain", label: "Knee Pain" },
    { id: "hip_joint_pain", label: "Hip Joint Pain" },
    { id: "muscle_weakness", label: "Muscle Weakness" },
    { id: "stiff_neck", label: "Stiff Neck" },
    { id: "swelling_joints", label: "Swelling Joints" },
    { id: "movement_stiffness", label: "Movement Stiffness" },
    { id: "spinning_movements", label: "Spinning Movements" },
    { id: "loss_of_balance", label: "Loss Of Balance" },
    { id: "unsteadiness", label: "Unsteadiness" },
    { id: "weakness_of_one_body_side", label: "Weakness Of One Body Side" },
    { id: "loss_of_smell", label: "Loss Of Smell" },
    { id: "bladder_discomfort", label: "Bladder Discomfort" },
    { id: "foul_smell_of_urine", label: "Foul Smell Of Urine" },
    { id: "continuous_feel_of_urine", label: "Continuous Feel Of Urine" },
    { id: "passage_of_gases", label: "Passage Of Gases" },
    { id: "internal_itching", label: "Internal Itching" },
    { id: "toxic_look_(typhos)", label: "Toxic Look (Typhos)" },
    { id: "depression", label: "Depression" },
    { id: "irritability", label: "Irritability" },
    { id: "muscle_pain", label: "Muscle Pain" },
    { id: "altered_sensorium", label: "Altered Sensorium" },
    { id: "red_spots_over_body", label: "Red Spots Over Body" },
    { id: "belly_pain", label: "Belly Pain" },
    { id: "abnormal_menstruation", label: "Abnormal Menstruation" },
    { id: "dischromic_patches", label: "Dischromic Patches" },
    { id: "watering_from_eyes", label: "Watering From Eyes" },
    { id: "increased_appetite", label: "Increased Appetite" },
    { id: "polyuria", label: "Polyuria" },
    { id: "family_history", label: "Family History" },
    { id: "mucoid_sputum", label: "Mucoid Sputum" },
    { id: "rusty_sputum", label: "Rusty Sputum" },
    { id: "lack_of_concentration", label: "Lack Of Concentration" },
    { id: "visual_disturbances", label: "Visual Disturbances" },
    { id: "receiving_blood_transfusion", label: "Receiving Blood Transfusion" },
    { id: "receiving_unsterile_injections", label: "Receiving Unsterile Injections" },
    { id: "coma", label: "Coma" },
    { id: "stomach_bleeding", label: "Stomach Bleeding" },
    { id: "distention_of_abdomen", label: "Distention Of Abdomen" },
    { id: "history_of_alcohol_consumption", label: "History Of Alcohol Consumption" },
    { id: "fluid_overload.1", label: "Fluid Overload" },
    { id: "blood_in_sputum", label: "Blood In Sputum" },
    { id: "prominent_veins_on_calf", label: "Prominent Veins On Calf" },
    { id: "palpitations", label: "Palpitations" },
    { id: "painful_walking", label: "Painful Walking" },
    { id: "pus_filled_pimples", label: "Pus Filled Pimples" },
    { id: "blackheads", label: "Blackheads" },
    { id: "scurring", label: "Scurring" },
    { id: "skin_peeling", label: "Skin Peeling" },
    { id: "silver_like_dusting", label: "Silver Like Dusting" },
    { id: "small_dents_in_nails", label: "Small Dents In Nails" },
    { id: "inflammatory_nails", label: "Inflammatory Nails" },
    { id: "blister", label: "Blister" },
    { id: "red_sore_around_nose", label: "Red Sore Around Nose" },
    { id: "yellow_crust_ooze", label: "Yellow Crust Ooze" }
];

const symptomContainer = document.getElementById('symptom-container');
const searchInput = document.getElementById('symptom-search');

// 2. Render Checkboxes into the UI
function renderSymptoms() {
    symptomContainer.innerHTML = '';
    allSymptoms.forEach(symp => {
        const div = document.createElement('div');
        div.className = 'symptom-item';
        div.innerHTML = `
            <input type="checkbox" id="${symp.id}" value="${symp.id}" class="symptom-checkbox">
            <label for="${symp.id}" class="symptom-label">${symp.label}</label>
        `;
        symptomContainer.appendChild(div);
    });
}

// Initialize checkbox list on load
renderSymptoms();

// 2.5 Selection Controls Logic
const btnSelectAll = document.getElementById('btn-select-all');
const btnClearAll = document.getElementById('btn-clear-all');
const symptomCounter = document.getElementById('symptom-counter');

function updateCounter() {
    const checkedCount = document.querySelectorAll('.symptom-checkbox:checked').length;
    symptomCounter.textContent = `Selected: ${checkedCount} symptom${checkedCount === 1 ? '' : 's'}`;
}

symptomContainer.addEventListener('change', function(e) {
    if (e.target && e.target.classList.contains('symptom-checkbox')) {
        updateCounter();
    }
});

btnSelectAll.addEventListener('click', function() {
    const checkboxes = document.querySelectorAll('.symptom-checkbox');
    checkboxes.forEach(cb => cb.checked = true);
    updateCounter();
});

btnClearAll.addEventListener('click', function() {
    const checkboxes = document.querySelectorAll('.symptom-checkbox');
    checkboxes.forEach(cb => cb.checked = false);
    updateCounter();
});

// 3. Search / Filter Logic
searchInput.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const items = symptomContainer.getElementsByClassName('symptom-item');
    let visibleCount = 0;
    
    Array.from(items).forEach(item => {
        const label = item.textContent.toLowerCase();
        if (label.includes(searchTerm)) {
            item.style.display = 'flex';
            visibleCount++;
        } else {
            item.style.display = 'none';
        }
    });

    const noMsg = document.getElementById('no-symptoms-msg');
    if (noMsg) {
        if (visibleCount === 0) {
            noMsg.style.display = 'block';
            symptomContainer.style.display = 'none';
        } else {
            noMsg.style.display = 'none';
            symptomContainer.style.display = 'block';
        }
    }
});

// 4. Form Submit Logic with Validation
document.getElementById('symptom-form').addEventListener('submit', async function(e) {
    e.preventDefault(); 

    const errorMessage = document.getElementById('error-message');
    const resultContainer = document.getElementById('result-container');
    
    // Reset previous states
    resultContainer.classList.remove('show');
    resultContainer.classList.add('hidden');
    errorMessage.classList.add('hidden');

    // Find all checked boxes and extract their values
    const checkedBoxes = document.querySelectorAll('.symptom-checkbox:checked');
    const userSymptoms = Array.from(checkedBoxes).map(cb => cb.value);
    
    // Validation 1: Empty check
    if (userSymptoms.length === 0) {
        errorMessage.textContent = "Please select at least one symptom.";
        errorMessage.classList.remove('hidden');
        return;
    }
    
    // Validation 2: Check if symptoms exist in the valid dataset
    const validIds = allSymptoms.map(s => s.id);
    const isValid = userSymptoms.every(s => validIds.includes(s));
    
    if (!isValid) {
        errorMessage.textContent = "No valid symptoms detected.";
        errorMessage.classList.remove('hidden');
        return;
    }
    
    // UI Elements for Loading and Request
    const loader = document.getElementById('loader');
    const submitBtn = document.getElementById('submit-btn');

    loader.classList.remove('hidden');
    submitBtn.disabled = true;

    try {
        // Send data as JSON
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symptoms: userSymptoms })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || 'Server returned an error');
        }

        const data = await response.json();

        // Populate Simple Text Data
        document.getElementById('res-disease').textContent = data.disease;
        
        // Update Confidence Score
        const badge = document.querySelector('.badge-confidence');
        if (badge && data.confidence_score !== undefined) {
            let label = "High Confidence";
            if (data.confidence_score < 60) label = "Low Confidence";
            else if (data.confidence_score < 80) label = "Moderate Confidence";
            badge.textContent = `${label} (${data.confidence_score}%)`;
        }
        document.getElementById('res-description').textContent = data.description;
        
        // Professional Disclaimer
        document.getElementById('res-disclaimer').textContent = "This application provides educational information regarding potential clinical treatments associated with these conditions. The treatments listed are NOT Over-The-Counter (OTC) recommendations, and most require a strict doctor's prescription. This tool does not replace professional medical diagnosis or treatment. NEVER start or change any medication without consulting a qualified healthcare provider.";

        // Populate Medications List with Icons and Spacing
        const medList = document.getElementById('res-medications');
        medList.innerHTML = ''; 
        
        let medicationsArray = data.medications;
        if (typeof medicationsArray === 'string') {
            try {
                let validJsonString = medicationsArray.replace(/'/g, '"');
                medicationsArray = JSON.parse(validJsonString);
            } catch (e) {
                medicationsArray = [medicationsArray];
            }
        }
        
        if (Array.isArray(medicationsArray)) {
            medicationsArray.forEach(med => {
                const li = document.createElement('li');
                li.textContent = med;
                medList.appendChild(li);
            });
        }
        
        // Trigger Smart Safety Check
        performSafetyCheck(medicationsArray);

        // Populate Precautions List
        const precList = document.getElementById('res-precautions');
        precList.innerHTML = '';
        if (Array.isArray(data.precautions)) {
            data.precautions.forEach(prec => {
                const li = document.createElement('li');
                li.textContent = prec;
                precList.appendChild(li);
            });
        }

        // Hide loader and show results with animation
        loader.classList.add('hidden');
        resultContainer.classList.remove('hidden');
        setTimeout(() => {
            resultContainer.classList.add('show');
        }, 50);

    } catch (error) {
        console.error("Error during prediction:", error);
        loader.classList.add('hidden');
        errorMessage.textContent = "Oops! Something went wrong. Please check your backend terminal for errors.";
        errorMessage.classList.remove('hidden');
    } finally {
        submitBtn.disabled = false;
    }
});

// 5. User Feedback System Logic
const starContainer = document.getElementById('star-container');
const ratingInput = document.getElementById('feedback-rating');
const feedbackForm = document.getElementById('feedback-form');
const feedbackError = document.getElementById('feedback-error');
const feedbackSuccess = document.getElementById('feedback-success');
const feedbackFormContainer = document.getElementById('feedback-form-container');

if (starContainer) {
    const stars = starContainer.querySelectorAll('.star');
    
    stars.forEach(star => {
        star.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            ratingInput.value = value;
            
            // Highlight stars up to the clicked one
            stars.forEach(s => {
                if (parseInt(s.getAttribute('data-value')) <= parseInt(value)) {
                    s.style.color = '#f1c40f'; // Gold
                } else {
                    s.style.color = '#ddd'; // Gray
                }
            });
        });
    });

    feedbackForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        feedbackError.classList.add('hidden');
        feedbackSuccess.classList.add('hidden');
        
        try {
            const response = await fetch('/user/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    rating: ratingInput.value,
                    comments: document.getElementById('feedback-comments') ? document.getElementById('feedback-comments').value : ''
                })
            });
            
            const data = await response.json();
            
            if (response.ok && data.status === 'success') {
                feedbackFormContainer.style.display = 'none';
                feedbackSuccess.classList.remove('hidden');
            } else {
                throw new Error(data.message || 'Server error');
            }
        } catch (error) {
            feedbackError.textContent = error.message;
            feedbackError.classList.remove('hidden');
        }
    });
}

function findNearbyHospitals(btnElement) {
    const originalText = btnElement.innerHTML;
    btnElement.innerHTML = "⏳ Locating...";
    btnElement.disabled = true;

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                const mapsUrl = `https://www.google.com/maps/search/hospitals/@${lat},${lng},14z`;
                window.open(mapsUrl, '_blank');
                btnElement.innerHTML = originalText;
                btnElement.disabled = false;
            },
            function(error) {
                alert('❌ Unable to access your location. Please ensure location services are enabled.');
                btnElement.innerHTML = originalText;
                btnElement.disabled = false;
            }
        );
    } else {
        alert('❌ Geolocation is not supported by this browser.');
        btnElement.innerHTML = originalText;
        btnElement.disabled = false;
    }
}

async function performSafetyCheck(medicinesArray) {
    const safetyContainer = document.getElementById('safety-warning-container');
    if (!safetyContainer) return;

    try {
        const response = await fetch('/user/safety-check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ medicines: medicinesArray })
        });

        if (response.status === 401) {
            safetyContainer.style.display = 'none';
            return;
        }

        if (!response.ok) {
            safetyContainer.style.display = 'none';
            return;
        }

        const data = await response.json();
        safetyContainer.style.display = 'block';
        
        let htmlContent;
        if (data.message) {
            htmlContent = `
                <div class="card warning-card clinical-border" style="border-left-color: #f39c12; background-color: #fdfaf3;">
                    <h3 class="section-title text-warning" style="margin-bottom: 5px;"><span class="icon">&#8505;</span> Safety Check Unavailable</h3>
                    <p class="text-muted small mb-0">${data.message}</p>
                </div>
            `;
        } else if (data.warnings && data.warnings.length > 0) {
            let warningsHtml = data.warnings.map(w => `<li style="color: #c0392b; font-weight: bold; margin-bottom: 5px;">${w}</li>`).join('');
            htmlContent = `
                <div class="card error-card clinical-border" style="border-left: 5px solid #e74c3c; background-color: #fdf3f2; padding: 20px; border-radius: 8px;">
                    <h3 class="section-title text-danger" style="margin-bottom: 10px; color: #c0392b;"><span class="icon">&#9888;</span> Critical Safety Warning</h3>
                    <p style="color: #c0392b; margin-bottom: 15px;">Based on your medical profile, the following conflicts were detected:</p>
                    <ul style="margin-bottom: 15px; padding-left: 20px;">
                        ${warningsHtml}
                    </ul>
                    <p class="text-muted small mb-0" style="font-weight: bold;">STOP: Do not take these medications without consulting a certified doctor or pharmacist immediately.</p>
                </div>
            `;
        } else {
            let safeChecksHtml = data.safe_checks ? data.safe_checks.map(s => `<li style="color: #27ae60; margin-bottom: 5px;">[+] ${s}</li>`).join('') : '';
            let unknownsHtml = data.unknowns ? data.unknowns.map(u => `<li style="color: #f39c12; margin-bottom: 5px;">[?] ${u}</li>`).join('') : '';
            
            htmlContent = `
                <div class="card success-card clinical-border" style="border-left: 5px solid #2ecc71; background-color: #f0fbf4; padding: 20px; border-radius: 8px;">
                    <h3 class="section-title text-success" style="margin-bottom: 10px; color: #27ae60;"><span class="icon">[OK]</span> Smart Safety Check Passed</h3>
                    <ul style="margin-bottom: 15px; padding-left: 20px; list-style-type: none;">
                        ${safeChecksHtml}
                        ${unknownsHtml}
                    </ul>
                    <p class="text-muted small mb-0"><strong>Disclaimer:</strong> This is an informational safety check and does not replace professional medical advice. Never assume a medicine is completely safe for your specific biology.</p>
                </div>
            `;
        }

        safetyContainer.innerHTML = htmlContent;

    } catch (e) {
        console.error("Safety Check Error:", e);
        safetyContainer.style.display = 'none';
    }
}
