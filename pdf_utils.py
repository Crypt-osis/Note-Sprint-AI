from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def create_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    title = data.get("title", "Study Notes")
    story.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    # Summary
    story.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
    story.append(Spacer(1, 8))

    for section in data.get("summary", []):
        story.append(Paragraph(f"<b>{section['heading']}</b>", styles["Heading3"]))
        bullets = [ListItem(Paragraph(point, styles["BodyText"])) for point in section["points"]]
        story.append(ListFlowable(bullets, bulletType='bullet'))
        story.append(Spacer(1, 8))

    # Key Terms
    story.append(Paragraph("<b>Key Terms</b>", styles["Heading2"]))
    story.append(Spacer(1, 8))

    for item in data.get("keyTerms", []):
        story.append(Paragraph(f"<b>{item['term']}</b>: {item['definition']}", styles["BodyText"]))
        story.append(Spacer(1, 6))

    # Quiz
    story.append(Paragraph("<b>Quiz</b>", styles["Heading2"]))
    story.append(Spacer(1, 8))

    for i, q in enumerate(data.get("quiz", []), start=1):
        story.append(Paragraph(f"<b>Q{i}. {q['question']}</b>", styles["BodyText"]))
        for option in q["options"]:
            story.append(Paragraph(f"• {option}", styles["BodyText"]))
        story.append(Paragraph(f"<b>Answer:</b> {q['answer']}", styles["BodyText"]))
        story.append(Spacer(1, 10))

    doc.build(story)
    buffer.seek(0)
    return buffer