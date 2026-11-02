import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime

def calculate_bmi(height_m, weight_kg):
    if not height_m or not weight_kg or height_m <= 0:
        return "N/A"
    try:
        bmi = weight_kg / (height_m ** 2)
        return f"{bmi:.1f}"
    except:
        return "N/A"

def calculate_water_intake(weight_kg):
    if not weight_kg or weight_kg <= 0:
        return "N/A"
    try:
        # roughly 35ml per kg
        intake_liters = (weight_kg * 35) / 1000
        return f"{intake_liters:.1f} Liters"
    except:
        return "N/A"

def generate_prediction_pdf(user, prediction_data):
    """
    Generates an in-memory PDF report for a prediction.
    user: dict with full_name, age, gender, height, weight
    prediction_data: dict with selected_symptoms, predicted_disease, medicines, precautions, timestamp
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=20,
        alignment=1 # Center
    )
    
    heading_style = ParagraphStyle(
        name='HeadingStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#3498db'),
        spaceBefore=15,
        spaceAfter=10
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 11
    normal_style.leading = 14
    
    bold_style = ParagraphStyle(name='BoldStyle', parent=normal_style, fontName='Helvetica-Bold')

    elements = []
    
    # Title
    elements.append(Paragraph("AI Medical Assistant - Prediction Report", title_style))
    
    # Date
    report_date = prediction_data.get('timestamp', datetime.now())
    if not isinstance(report_date, datetime):
        # Fallback if timestamp is a string
        report_date = datetime.now()
    date_str = report_date.strftime("%B %d, %Y - %I:%M %p")
    elements.append(Paragraph(f"<b>Date:</b> {date_str}", normal_style))
    elements.append(Spacer(1, 15))
    
    # Patient Information
    elements.append(Paragraph("Patient Profile", heading_style))
    
    raw_height = user.get('height')
    raw_weight = user.get('weight')
    
    try:
        height = float(raw_height) if raw_height else None
        weight = float(raw_weight) if raw_weight else None
    except (ValueError, TypeError):
        height = None
        weight = None
    
    # We don't know if height is cm or meters, let's assume cm if > 3, meters if < 3.
    bmi_val = "N/A"
    if height and weight:
        h_m = height if height < 3 else height / 100
        bmi_val = calculate_bmi(h_m, weight)
        
    water_val = calculate_water_intake(weight) if weight else "N/A"
    
    patient_data = [
        ['Name:', user.get('full_name', 'Unknown'), 'Age:', str(user.get('age', 'N/A'))],
        ['Gender:', user.get('gender', 'N/A'), 'BMI:', bmi_val],
        ['Height:', str(height) if height else 'N/A', 'Water Target:', water_val],
        ['Weight:', str(weight) if weight else 'N/A', '', '']
    ]
    
    ptable = Table(patient_data, colWidths=[80, 150, 80, 150])
    ptable.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#2c3e50')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8f9fa')),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.white),
        ('BOX', (0,0), (-1,-1), 0.25, colors.white),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    elements.append(ptable)
    elements.append(Spacer(1, 20))
    
    # Symptoms
    elements.append(Paragraph("Reported Symptoms", heading_style))
    symptoms = prediction_data.get('selected_symptoms', [])
    symp_text = ", ".join([s.replace('_', ' ').title() for s in symptoms]) if symptoms else "None reported"
    elements.append(Paragraph(symp_text, normal_style))
    elements.append(Spacer(1, 10))
    
    # Prediction
    elements.append(Paragraph("Clinical Prediction", heading_style))
    disease = prediction_data.get('predicted_disease', 'Unknown')
    elements.append(Paragraph(f"<b>Predicted Condition:</b> {disease}", normal_style))
    elements.append(Spacer(1, 10))
    
    # Helper to parse lists stored as strings
    import ast
    def parse_data_list(data):
        if isinstance(data, list): return data
        if isinstance(data, str):
            try:
                parsed = ast.literal_eval(data)
                if isinstance(parsed, list): return parsed
            except: pass
            return [x.strip() for x in data.split(',')]
        return []

    # Medicines
    elements.append(Paragraph("Suggested Over-the-Counter (OTC) Medicines", heading_style))
    medicines = parse_data_list(prediction_data.get('medicines', []))
    if medicines:
        for med in medicines:
            med_clean = str(med).strip(" '\"[]")
            if med_clean:
                elements.append(Paragraph(f"• {med_clean}", normal_style))
    else:
        elements.append(Paragraph("No specific medicines recommended for this condition.", normal_style))
    elements.append(Spacer(1, 10))
    
    # Precautions
    elements.append(Paragraph("Recommended Precautions", heading_style))
    precautions = parse_data_list(prediction_data.get('precautions', []))
    if precautions:
        for pre in precautions:
            pre_clean = str(pre).strip(" '\"[]")
            if pre_clean:
                elements.append(Paragraph(f"• {pre_clean.capitalize()}", normal_style))
    else:
        elements.append(Paragraph("No specific precautions listed.", normal_style))
    elements.append(Spacer(1, 25))
    
    # Disclaimer
    disclaimer_style = ParagraphStyle(
        name='DisclaimerStyle',
        parent=styles['Italic'],
        fontSize=9,
        textColor=colors.HexColor('#e74c3c'),
        leading=12
    )
    elements.append(Paragraph("<b>DISCLAIMER:</b> This report is generated by an AI model based on the symptoms provided. It is for informational purposes only and does not constitute professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider with any questions you may have regarding a medical condition. Do not self-medicate.", disclaimer_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
