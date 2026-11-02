import os

template_dir = r"c:\Users\ABHINAV SAJU\Downloads\Medicine_Recommendation_System\templates"

replacements = {
    # It seems the mangled characters are a mix of bytes. We can use context-based replacement to be safe.
    'style="color: #3498db;">dYc</span> AI Medical Assistant': 'style="color: #3498db;">🩺</span> AI Medical Assistant',
    'style="color: #3498db;">dYcï¿½</span> AI Medical Assistant': 'style="color: #3498db;">🩺</span> AI Medical Assistant',
    
    'title="Toggle Dark Mode">dYOT</button>': 'title="Toggle Dark Mode">🌙</button>',
    'title="Toggle Dark Mode">dYOT</button>': 'title="Toggle Dark Mode">🌙</button>',
    
    'color: #a0aec0; font-size: 1.2rem;">dY"?</span>': 'color: #a0aec0; font-size: 1.2rem;">🔍</span>',
    
    'text-white m-0">dYc Predicted Condition': 'text-white m-0">🩺 Predicted Condition',
    'text-white m-0">dYcï¿½ Predicted Condition': 'text-white m-0">🩺 Predicted Condition',
    
    '<span class="icon">dY\'S</span> Potential Treatments': '<span class="icon">💊</span> Potential Treatments',
    
    '<span class="icon">dY>,?</span> Recommended Precautions': '<span class="icon">⚠️</span> Recommended Precautions',
    '<span class="icon">dY>ï¿½,?</span> Recommended Precautions': '<span class="icon">⚠️</span> Recommended Precautions',
    
    '<span class="icon">dY?</span> Find Nearby Hospitals': '<span class="icon">🏥</span> Find Nearby Hospitals',
    '<span class="icon">dY?ï¿½</span> Find Nearby Hospitals': '<span class="icon">🏥</span> Find Nearby Hospitals',

    # user/dashboard.html specific
    'dY\'b Welcome back': '👋 Welcome back',
    'dY\' Daily Health Tip': '💡 Daily Health Tip',
    
    # Check if there are other known mangled ones
    'dY"œ Prediction History': '📜 Prediction History',
    'dY"¥ PDF': '📥 PDF',
    'dY"œ PDF': '📥 PDF',
    'âœ‰ï¸ Email': '✉️ Email',
    'dY"¥ Email': '✉️ Email'
}

for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            modified = False
            
            # Add meta charset if missing
            if '<meta charset="UTF-8">' not in content and '<head>' in content:
                content = content.replace('<head>', '<head>\n    <meta charset="UTF-8">')
                modified = True
                
            # Perform replacements
            for old, new in replacements.items():
                if old in content:
                    content = content.replace(old, new)
                    modified = True
            
            # Additional aggressive cleanup for common isolated mangled chars if context wasn't perfect
            if 'dYc' in content: content = content.replace('dYc', '🩺'); modified = True
            if 'dYOT' in content: content = content.replace('dYOT', '🌙'); modified = True
            if 'dY"?' in content: content = content.replace('dY"?', '🔍'); modified = True
            if 'dY\'S' in content: content = content.replace('dY\'S', '💊'); modified = True
            if 'dY>,?' in content: content = content.replace('dY>,?', '⚠️'); modified = True
            if 'dY?' in content: content = content.replace('dY?', '🏥'); modified = True
            if 'dY\'b' in content: content = content.replace('dY\'b', '👋'); modified = True
            if 'dY\'' in content and 'dY\'S' not in content: content = content.replace('dY\'', '💡'); modified = True
            if 'dY"œ' in content: content = content.replace('dY"œ', '📜'); modified = True
            if 'dY"¥' in content: content = content.replace('dY"¥', '📥'); modified = True

            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed {file}")

print("Done fixing HTML emojis.")
