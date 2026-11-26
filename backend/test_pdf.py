from pdf_reports.generator import generate_clinical_report

print("Generating PDF report...")

report_data = {
    "patient_name": "Γιώργος Παπαδόπουλος",
    "date_of_birth": "01/01/1980",
    "examination_date": "26/11/2026",
    "clinical_findings": (
        "Ο ασθενής προσήλθε για οδοντιατρική εξέταση. "
        "Παρατηρήθηκε οστική υφίζηση στην περιοχή των "
        "οπισθίων δοντιών."
    )
}

pdf = generate_clinical_report(report_data)

with open("test_report.pdf", "wb") as file:
    file.write(pdf.getvalue())

print("PDF generated successfully!")