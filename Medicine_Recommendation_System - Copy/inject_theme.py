import os
import re

template_dir = r"c:\Users\ABHINAV SAJU\Downloads\Medicine_Recommendation_System\templates"

fouc_script = """
    <script>
        if (localStorage.getItem('theme') === 'dark') {
            document.documentElement.classList.add('dark-mode');
        }
    </script>
"""

theme_js_tag = """
<script src="{{ url_for('static', filename='js/theme.js') }}"></script>
"""

toggle_btn = """<button class="nav-btn-ghost theme-toggle-btn" onclick="toggleTheme()" style="background: none; border: none; font-size: 1.2rem; cursor: pointer;" title="Toggle Dark Mode">🌙</button>"""

for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            modified = False
            
            # 1. Inject FOUC
            if "localStorage.getItem('theme')" not in content and "</head>" in content:
                content = content.replace("</head>", fouc_script + "</head>")
                modified = True
                
            # 2. Inject JS tag
            if "theme.js" not in content and "</body>" in content:
                content = content.replace("</body>", theme_js_tag + "</body>")
                modified = True
                
            # 3. Inject Button
            if "toggleTheme()" not in content:
                # User navs
                user_nav_marker = '<div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">'
                if user_nav_marker in content:
                    content = content.replace(user_nav_marker, user_nav_marker + '\n            ' + toggle_btn)
                    modified = True
                # Admin navs
                admin_nav_marker = '<nav style="display: flex; gap: 15px; background: #f8f9fa; padding: 10px 15px; border-radius: 6px; border: 1px solid #e9ecef;">'
                if admin_nav_marker in content:
                    content = content.replace(admin_nav_marker, admin_nav_marker + '\n            ' + toggle_btn)
                    modified = True
                # Landing nav
                landing_nav_marker = '<div class="nav-links">'
                if landing_nav_marker in content:
                    content = content.replace(landing_nav_marker, landing_nav_marker + '\n                ' + toggle_btn)
                    modified = True

            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {file}")

print("Done injecting HTML.")
