from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def generate_pdf(patient):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>Heart Disease Prediction Report</b>", styles["Title"]))
    story.append(Paragraph(f"<b>Name:</b> {patient.name}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Email:</b> {patient.email}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Phone:</b> {patient.phone}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Age:</b> {patient.age}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Gender:</b> {patient.gender}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Prediction:</b> {patient.prediction}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Confidence:</b> {patient.confidence}%", styles["BodyText"]))

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf