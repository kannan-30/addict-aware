"""
Antigravity - Addict Aware
PDF Report Generator

Generates downloadable PDF progress reports for users.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime


def generate_progress_report(user_name, assessments, tips):
    """
    Generate a PDF progress report for a user.

    Args:
        user_name: User's display name
        assessments: List of assessment dicts
        tips: List of health tips for the user

    Returns:
        BytesIO buffer containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5 * inch, bottomMargin=0.5 * inch)

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=22,
        textColor=colors.HexColor('#6C63FF'),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=20
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=15,
        spaceAfter=8
    )
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    story = []

    # Header
    story.append(Paragraph("Addict Aware", title_style))
    story.append(Paragraph(f"Progress Report for {user_name}", subtitle_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", body_style))
    story.append(HRFlowable(width="100%", color=colors.HexColor('#E2E8F0'), thickness=1, spaceAfter=15))

    # Summary Section
    if assessments:
        latest = assessments[0]
        story.append(Paragraph("Latest Assessment Summary", heading_style))
        story.append(Paragraph(f"Addiction Level: <b>{latest.get('addiction_level', 'N/A')}</b>", body_style))
        story.append(Paragraph(f"Addiction Score: <b>{latest.get('addiction_score', 'N/A')}/100</b>", body_style))
        story.append(Paragraph(f"Emotional State: <b>{latest.get('sentiment', 'N/A')}</b>", body_style))
        story.append(Spacer(1, 10))

    # Assessment History Table
    if assessments:
        story.append(Paragraph("Assessment History", heading_style))

        table_data = [['Date', 'Screen Time', 'Pickups', 'Social Media', 'Level', 'Score']]
        for a in assessments[:10]:  # Last 10 assessments
            date_str = a.get('created_at', datetime.utcnow()).strftime('%m/%d/%Y') if isinstance(a.get('created_at'), datetime) else str(a.get('created_at', ''))[:10]
            table_data.append([
                date_str,
                f"{a.get('screen_time', 0)}h",
                str(a.get('phone_pickups', 0)),
                f"{a.get('social_media_time', 0)}h",
                a.get('addiction_level', ''),
                str(a.get('addiction_score', ''))
            ])

        table = Table(table_data, colWidths=[80, 70, 60, 75, 60, 50])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6C63FF')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(table)
        story.append(Spacer(1, 15))

    # Health Tips
    if tips:
        story.append(Paragraph("Recommended Health Tips", heading_style))
        for tip in tips:
            story.append(Paragraph(f"• <b>{tip.get('title', '')}</b>: {tip.get('content', '')}", body_style))
        story.append(Spacer(1, 10))

    # Footer
    story.append(HRFlowable(width="100%", color=colors.HexColor('#E2E8F0'), thickness=1, spaceBefore=20))
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#94A3B8'))
    story.append(Paragraph("Addict Aware | Digital Wellness Platform | Confidential Report", footer_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
