import os

template_dir = r"c:\Users\ABHINAV SAJU\Downloads\Medicine_Recommendation_System\templates"

replacements = {
    "ðŸ©º": "🩺",
    "ðŸŒ™": "🌙",
    "ðŸ” ": "🔍",
    "âž”": "➔",
    "ðŸ’Š": "💊",
    "âš ï¸ ": "⚠️",
    "ðŸ ¥": "🏥",
    "ðŸ‘‹": "👋",
    "ðŸ’¡": "💡",
    "ðŸ“œ": "📜",
    "ðŸ“¥": "📥",
    "âœ‰ï¸ ": "✉️",
    "ðŸ›¡ï¸ ": "🛡️",
    "â„¹ï¸ ": "ℹ️",
    "âœ…": "✅",
    "â “": "❓"
}

for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            modified = False
            
            if '<meta charset="UTF-8">' not in content and '<head>' in content:
                content = content.replace('<head>', '<head>\n    <meta charset="UTF-8">')
                modified = True
                
            for old, new in replacements.items():
                if old in content:
                    content = content.replace(old, new)
                    modified = True

            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed {file}")

print("Done fixing HTML emojis.")
