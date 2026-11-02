import os

filepath = r'c:\Users\ABHINAV SAJU\Downloads\Medicine_Recommendation_System\templates\index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

bad_chunk = '''                <!-- Precautions -->
                <div class="card precautions-card clinical-border">
                <p class="text-muted" style="margin-bottom: 15px;">Was this prediction helpful? Let us know!</p>'''

good_chunk = '''                <!-- Precautions -->
                <div class="card precautions-card clinical-border">
                    <h3 class="section-title text-warning"><span class="icon">🛡️</span> Recommended Precautions</h3>
                    <p class="text-muted small mb-3">General guidelines to help manage your condition:</p>
                    <ul id="res-precautions" class="checklist mt-2"></ul>
                </div>
            </div>

            <!-- Medical Disclaimer & Hospitals -->
            <div class="card warning-card mt-4">
                <div style="display: flex; gap: 15px; align-items: flex-start;">
                    <div style="font-size: 2rem;">⚠️</div>
                    <div>
                        <h3 class="warning-title m-0">Important Medical Disclaimer</h3>
                        <p id="res-disclaimer" class="warning-text mt-2 mb-2"></p>
                        <hr style="border: 0; border-top: 1px solid rgba(0,0,0,0.1); margin: 10px 0;">
                        <p class="warning-text mb-2" style="font-weight: 600;">For urgent or severe symptoms, seek professional medical care. Find nearby healthcare facilities.</p>
                        <button onclick="findNearbyHospitals()" class="nav-btn-outline" style="border-color: #e74c3c; color: #e74c3c; display: inline-flex; align-items: center; gap: 5px;">
                            <span class="icon">🏥</span> Find Nearby Hospitals
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- User Feedback System -->
            {% if session.get('user_id') %}
            <div class="card mt-4" id="feedback-card" style="background-color: #f8f9fa; border: 1px solid #e9ecef; text-align: center;">
                <h3 class="section-title" style="margin-bottom: 15px; color: #2c3e50;">⭐ Rate Your Experience</h3>
                <p class="text-muted" style="margin-bottom: 15px;">Was this prediction helpful? Let us know!</p>'''

if bad_chunk in text:
    text = text.replace(bad_chunk, good_chunk)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed index.html perfectly.')
else:
    print('Bad chunk not found in index.html.')
