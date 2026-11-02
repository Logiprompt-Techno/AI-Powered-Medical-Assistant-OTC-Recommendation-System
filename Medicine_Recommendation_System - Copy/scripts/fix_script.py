import re

filepath = r'c:\Users\ABHINAV SAJU\Downloads\Medicine_Recommendation_System\static\js\script.js'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the entire broken function
start_idx = text.find('function findNearbyHospitals(btnElement) {')
if start_idx != -1:
    # Just truncate everything from that point onwards
    text = text[:start_idx]

correct_js = """function findNearbyHospitals(btnElement) {
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
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text + correct_js)

print('Fixed script.js')
