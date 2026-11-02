import os

filepath = r'c:\Users\ABHINAV SAJU\Downloads\Medicine_Recommendation_System\templates\user\dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

js_code = '''
    function findNearbyHospitals(btnElement) {
        const originalText = btnElement.innerHTML;
        btnElement.innerHTML = "⏳ Locating...";
        btnElement.disabled = true;

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;
                    const mapsUrl = https://www.google.com/maps/search/hospitals/@,,14z;
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
'''

target = '</script>'
if target in text:
    text = text.replace(target, js_code + '\n</script>')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Added JS to dashboard.html')
else:
    print('Target not found in dashboard.html')

# Now add to static/js/script.js for index.html
js_path = r'c:\Users\ABHINAV SAJU\Downloads\Medicine_Recommendation_System\static\js\script.js'
with open(js_path, 'a', encoding='utf-8') as f:
    f.write('\n' + js_code)
print('Added JS to script.js')
