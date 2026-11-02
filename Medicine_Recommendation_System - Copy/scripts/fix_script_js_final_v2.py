with open(r'c:\Users\ABHINAV SAJU\Downloads\Medicine_Recommendation_System\static\js\script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if line.strip() == "precList.innerHTML = '';":
        break

rest = r'''        if (Array.isArray(data.precautions)) {
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
'''

with open(r'c:\Users\ABHINAV SAJU\Downloads\Medicine_Recommendation_System\static\js\script.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
    f.write(rest)

print('Restored script.js completely via python.')
