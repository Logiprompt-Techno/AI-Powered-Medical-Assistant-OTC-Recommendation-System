import re

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='latin-1') as f:
            text = f.read()

    # Generic replacements
    text = text.replace('ðŸ“œ', '📜')
    text = text.replace('ðŸ“¥', '📥')
    text = text.replace('ðŸ“‹', '📭')
    text = text.replace('â† ', '⬅️')
    text = text.replace('âœ‰ï¸', '✉️')
    text = text.replace('â\x8f³', '⏳')
    text = text.replace('? Sending...', '⏳ Sending...')
    text = text.replace('ðŸ‘‹', '👋')
    text = text.replace('ðŸ’¡', '💡')
    text = text.replace('ðŸ”„', '🔄')
    
    # Just to be sure, also do regexes for email btn
    text = re.sub(r'>\s*?\?\s+Email', '> ✉️ Email', text)
    text = re.sub(r'innerText = "\?\s+Sending', 'innerText = "⏳ Sending', text)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

fix_file('c:\\Users\\ABHINAV SAJU\\Downloads\\Medicine_Recommendation_System\\templates\\history.html')
fix_file('c:\\Users\\ABHINAV SAJU\\Downloads\\Medicine_Recommendation_System\\templates\\user\\dashboard.html')
print('Emojis fixed.')
