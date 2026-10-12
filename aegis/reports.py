import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def generate_pdf_report(consultation_data, user_info):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []
    
    # Enhanced title with logo placeholder
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=30,
        textColor=colors.HexColor('#2E86AB'),
        alignment=1  # Center alignment
    )
    story.append(Paragraph("🩺 AEGIS HEALTH", title_style))
    story.append(Paragraph("Comprehensive Medical Consultation Report", styles['Heading2']))
    story.append(Spacer(1, 20))
    
    # Patient information table
    patient_data = [
        ['Patient Information', ''],
        ['Username:', user_info['username']],
        ['User Type:', user_info.get('user_type', 'Patient').title()],
        ['Date of Consultation:', consultation_data['date']],
        ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    ]
    
    if user_info.get('medical_id'):
        patient_data.append(['Medical ID:', user_info['medical_id']])
    if user_info.get('specialization'):
        patient_data.append(['Specialization:', user_info['specialization']])
    
    patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 20))
    
    # Rest of the report content...
    # [Previous PDF content with enhancements]
    
    doc.build(story)
    buffer.seek(0)
    return buffer
