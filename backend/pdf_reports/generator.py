
from io import BytesIO
from pathlib import Path

from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


# --------------------------------------------------
# FONT CONFIGURATION
# --------------------------------------------------

FONT_PATH = Path(__file__).parent / "fonts" / "DejaVuSans.ttf"

pdfmetrics.registerFont(
    TTFont("DejaVu", str(FONT_PATH))
)


# --------------------------------------------------
# DOCUMENT STYLES
# --------------------------------------------------

styles = getSampleStyleSheet()

styles.add(
    ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="DejaVu",
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#243447"),
        spaceAfter=8
    )
)

styles.add(
    ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontName="DejaVu",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#243447"),
        spaceBefore=12,
        spaceAfter=6
    )
)

styles.add(
    ParagraphStyle(
        name="ReportBody",
        parent=styles["BodyText"],
        fontName="DejaVu",
        fontSize=10,
        leading=15,
        alignment=TA_LEFT,
        spaceAfter=6
    )
)


# --------------------------------------------------
# PDF GENERATOR
# --------------------------------------------------

def generate_clinical_report(report_data):

    # Create an in-memory PDF file.
    pdf_buffer = BytesIO()

    # Configure the document.
    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    # This list contains all elements of the PDF.
    story = []

    # Report title.
    story.append(
        Paragraph(
            "Κλινική Οδοντιατρική Αναφορά",
            styles["ReportTitle"]
        )
    )

    story.append(Spacer(1, 10 * mm))

    # Patient information section.
    story.append(
        Paragraph(
            "Στοιχεία Ασθενούς",
            styles["SectionHeading"]
        )
    )

    patient_name = escape(str(report_data.get("patient_name") or "Δεν έχει καταχωρηθεί"))
    date_of_birth = escape(str(report_data.get("date_of_birth") or "Δεν έχει καταχωρηθεί"))
    examination_date = escape(str(report_data.get("examination_date") or "Δεν έχει καταχωρηθεί"))

    patient_data = [
        ["Ονοματεπώνυμο:", patient_name],
        ["Ημερομηνία Γέννησης:", date_of_birth],
        ["Ημερομηνία Εξέτασης:", examination_date]
    ]

    patient_table = Table(
        patient_data,
        colWidths=[55 * mm, 110 * mm]
    )

    patient_table.setStyle(
        TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#333333")),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef2f6")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(patient_table)

    # Clinical findings section.
    story.append(
        Paragraph(
            "Κλινικά Ευρήματα",
            styles["SectionHeading"]
        )
    )

    clinical_text = escape(
        str(
            report_data.get("clinical_findings")
            or "Δεν έχουν καταχωριστεί κλινικά ευρήματα."
        )
    )

    story.append(
        Paragraph(
            clinical_text,
            styles["ReportBody"]
        )
    )

    # Generate the PDF.
    document.build(story)

    # Return the PDF from the beginning of the buffer.
    pdf_buffer.seek(0)

    return pdf_buffer
