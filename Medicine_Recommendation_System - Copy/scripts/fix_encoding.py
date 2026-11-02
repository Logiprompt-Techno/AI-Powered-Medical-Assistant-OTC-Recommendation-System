import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='latin-1') as f:
        text = f.read()

    text = re.sub(r'<h1>.*? Prediction History</h1>', r'<h1>?? Prediction History</h1>', text)
    text = re.sub(r'<div style="font-size: 3\.5rem; margin-bottom: 10px;">.*?</div>', r'<div style="font-size: 3.5rem; margin-bottom: 10px;">??</div>', text)
    text = re.sub(r'<a href="/" class="back-btn">.*? Back to Predictor</a>', r'<a href="/" class="back-btn">?? Back to Predictor</a>', text)
    
    text = re.sub(r'dY" PDF', '?? PDF', text)
    text = re.sub(r'dY" PDF', '?? PDF', text)
    text = re.sub(r'âœ‰ï¸ Email', '?? Email', text)
    text = re.sub(r'â\x8f³ Sending...', '? Sending...', text)
    text = re.sub(r'\? Sending...', '? Sending...', text)
    
    # Dashboard specific
    text = re.sub(r'<span class="icon" style="color: #3498db;">.*?</span> Welcome,', r'<span class="icon" style="color: #3498db;">??</span> Welcome,', text)
    text = re.sub(r'<span class="icon">.*?</span> Daily Health Tip', r'<span class="icon">??</span> Daily Health Tip', text)
    text = re.sub(r'title="Get a new tip">.*?<', r'title="Get a new tip">??<', text, flags=re.DOTALL)
    
    # Just generic fix for garbled emojis
    text = text.replace('dY"o', '??').replace('dY"', '??').replace('dY"<', '??')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

fix_file('c:\\Users\\ABHINAV SAJU\\Downloads\\Medicine_Recommendation_System\\templates\\history.html')
fix_file('c:\\Users\\ABHINAV SAJU\\Downloads\\Medicine_Recommendation_System\\templates\\user\\dashboard.html')
print('Fixed encoding issues.')
