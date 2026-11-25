print("Generating PDF report...")
      
from pdf_reports.generator import generate_clinical_report

print("Import successful!")

pdf = generate_clinical_report()

print("PDF generation complete. Saving to file...")

with open("test_report.pdf", "wb") as file:
    file.write(pdf.getvalue())

print("PDF generated successfully!")