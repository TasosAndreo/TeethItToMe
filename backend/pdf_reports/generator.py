
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Locate the font file relative to this Python file.
FONT_PATH = Path(__file__).parent / "fonts" / "DejaVuSans.ttf"

# Register the Unicode font.
pdfmetrics.registerFont(
    TTFont("DejaVu", str(FONT_PATH))
)


def generate_clinical_report():
    # Create an in-memory file for the PDF.
    pdf_buffer = BytesIO()

    # Create a PDF canvas using A4 dimensions.
    pdf = canvas.Canvas(pdf_buffer, pagesize=A4)

    # Get the width and height of the A4 page.
    page_width, page_height = A4

    # Add the report title.
    pdf.setFont("DejaVu", 18)
    pdf.drawString(50, page_height - 60, "Κλινική Οδοντιατρική Αναφορά")

    # Add some introductory text.
    pdf.setFont("DejaVu", 12)
    pdf.drawString(50, page_height - 100, "Ασθενής: Παράδειγμα Ασθενούς")

    # Finalize the PDF.
    pdf.save()

    # Move the buffer position to the beginning.
    pdf_buffer.seek(0)

    return pdf_buffer