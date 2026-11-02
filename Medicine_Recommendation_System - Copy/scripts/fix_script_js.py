with open(r'c:\Users\ABHINAV SAJU\Downloads\Medicine_Recommendation_System\static\js\script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if line.strip() == 'medicationsArray = JSON.parse(validJsonString);' and '{ id: "loss_of_smell", label: "Loss Of Smell" },' in lines[i+1]:
        new_lines.append(line)
        new_lines.append('            } catch (e) {\n')
        new_lines.append('                medicationsArray = [medicationsArray];\n')
        new_lines.append('            }\n')
        new_lines.append('        }\n')
        new_lines.append('        \n')
        new_lines.append('        if (Array.isArray(medicationsArray)) {\n')
        new_lines.append('            medicationsArray.forEach(med => {\n')
        new_lines.append('                const li = document.createElement(\'li\');\n')
        new_lines.append('                li.textContent = med;\n')
        new_lines.append('                medList.appendChild(li);\n')
        new_lines.append('            });\n')
        new_lines.append('        }\n')
        new_lines.append('        \n')
        new_lines.append('        // Trigger Smart Safety Check\n')
        new_lines.append('        performSafetyCheck(medicationsArray);\n')
        new_lines.append('\n')
        new_lines.append('        // Populate Precautions List\n')
        new_lines.append('        const precList = document.getElementById(\'res-precautions\');\n')
        new_lines.append('        precList.innerHTML = \'\';\n')
        skip = True
        continue
        
    if skip:
        if line.strip() == 'if (Array.isArray(data.precautions)) {':
            skip = False
            new_lines.append(line)
        continue
        
    new_lines.append(line)

with open(r'c:\Users\ABHINAV SAJU\Downloads\Medicine_Recommendation_System\static\js\script.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Restored script.js')
