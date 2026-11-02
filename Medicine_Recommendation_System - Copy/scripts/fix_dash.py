import os

filepath = r'c:\Users\ABHINAV SAJU\Downloads\Medicine_Recommendation_System\templates\user\dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

hospital_html = '''        <!-- Nearby Hospitals Card -->
        <div class="card mt-3" style="border-left: 4px solid #e74c3c; background: #fdf3f2;">
            <div style="display: flex; gap: 15px; align-items: center;">
                <div style="font-size: 2rem;">🏥</div>
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 5px 0; color: #c0392b; font-size: 1.1rem;">Emergency & Medical Facilities</h4>
                    <p style="margin: 0 0 10px 0; color: #e74c3c; font-size: 0.95rem; font-weight: 500;">For urgent or severe symptoms, seek professional medical care. Find nearby healthcare facilities.</p>
                    <button onclick="findNearbyHospitals(this)" class="nav-btn-outline" style="border-color: #c0392b; color: #c0392b; display: inline-flex; align-items: center; gap: 5px; padding: 6px 12px; border-radius: 4px; font-weight: bold; background: white; cursor: pointer;">
                        Find Nearby Hospitals
                    </button>
                </div>
            </div>
        </div>
'''

# Find a good place to insert it. Below the health tip card is good.
target = '''            <button onclick="generateRandomTip()" style="background: #e8f8f5; color: #1abc9c; border: 1px solid #1abc9c; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.3s; font-size: 1.2rem;" title="Get a new tip">
                🔄
            </button>
        </div>'''

if target in text:
    text = text.replace(target, target + '\n\n' + hospital_html)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Added hospital card to dashboard.html')
else:
    print('Target not found in dashboard.html')

