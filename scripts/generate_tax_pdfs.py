import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configuration data based on the missing information request and screenshot specifics!
TAX_DATA = {
    "US": {
        "title": "United States Tax Policies and Rates 2024",
        "income_tax": "10% to 37% progressive federal income tax.",
        "corporate_tax": "15-21% federal corporate tax rate.",
        "gst_vat": "No federal GST or VAT. State-level sales taxes apply.",
        "deduction_limit": "$10,000 (Form 2106 business expenses limit).",
        "tax_filing_deadline": "April 15th."
    },
    "UK": {
        "title": "United Kingdom Tax Policies and Rates 2024",
        "income_tax": "20% to 45% basic, higher, and additional rates.",
        "corporate_tax": "19-25% main rate depending on profits.",
        "gst_vat": "VAT ranges from 0% to 20% (standard rate).",
        "deduction_limit": "£1,000 (Basic Rate trading allowance deduction limit).",
        "tax_filing_deadline": "January 31st for online Self Assessment."
    },
    "AUSTRALIA": {
        "title": "Australia Tax Policies and Rates 2024",
        "income_tax": "19% to 45% progressive individual income tax.",
        "corporate_tax": "26-30% depending on base rate entity status.",
        "gst_vat": "10% standard GST on most goods and services.",
        "deduction_limit": "$300 (Work-Related Expenses without receipts limit).",
        "tax_filing_deadline": "October 31st."
    },
    "INDIA": {
        "title": "India Tax Policies and Rates 2024",
        "income_tax": "20-40% progressing based on new vs old tax regime slabs.",
        "corporate_tax": "22-25% depending on domestic company turnover status.",
        "gst_vat": "Multi-stage GST system with rates from 5% to 28%.",
        "deduction_limit": "₹50,000 (Standard deduction Section 80C / salaried individuals limit).",
        "tax_filing_deadline": "July 31st for individuals."
    },
    "CANADA": {
        "title": "Canada Tax Policies and Rates 2024",
        "income_tax": "15% to 33% progressive federal income tax plus provincial taxes.",
        "corporate_tax": "15% net federal corporate tax rate (after abatement).",
        "gst_vat": "5% federal GST plus provincial sales taxes (PST) or harmonized HST.",
        "deduction_limit": "$40,000 (Line 22900 other employment expenses limit).",
        "tax_filing_deadline": "April 30th."
    },
    "GERMANY": {
        "title": "Germany Tax Policies and Rates 2024",
        "income_tax": "14% to 45% progressive income tax (Einkommensteuer).",
        "corporate_tax": "15% corporate tax plus solidarity surcharge and trade tax.",
        "gst_vat": "19% standard VAT rate (reduced rate of 7%).",
        "deduction_limit": "€1,000 (Einkommensteuer income-related standard deduction limit).",
        "tax_filing_deadline": "July 31st."
    },
    "CHINA": {
        "title": "China Tax Policies and Rates 2024",
        "income_tax": "3% to 45% progressive Individual Income Tax (IIT).",
        "corporate_tax": "25% standard Enterprise Income Tax (EIT).",
        "gst_vat": "13% standard VAT rate with reduced rates of 9% and 6%.",
        "deduction_limit": "¥20,000 (Individual Income Tax specific annual deduction limit).",
        "tax_filing_deadline": "June 30th (for IIT annual reconciliation)."
    }
}

def create_pdf(country_code, data, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=14
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor("#2E3192"),
        spaceAfter=10
    )
    
    body_style = styles['Normal']
    
    flowables = []
    
    # Title
    flowables.append(Paragraph(data["title"], title_style))
    flowables.append(Spacer(1, 12))
    
    # Content Sections
    sections = [
        ("Income Tax Rates", data["income_tax"]),
        ("Corporate Tax Rates", data["corporate_tax"]),
        ("GST / VAT System", data["gst_vat"]),
        ("Deduction Limits", data["deduction_limit"]),
        ("Tax Filing Deadline", data["tax_filing_deadline"])
    ]
    
    for heading, text in sections:
        flowables.append(Paragraph(heading, heading_style))
        flowables.append(Paragraph(text, body_style))
        flowables.append(Spacer(1, 10))
        
    doc.build(flowables)
    print(f"Generated: {output_path}")


if __name__ == "__main__":
    pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "PDF")
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
        
    for country, details in TAX_DATA.items():
        country_folder = os.path.join(pdf_dir, country)
        if not os.path.exists(country_folder):
            os.makedirs(country_folder)
            
        pdf_path = os.path.join(country_folder, f"{country}_Tax_Info.pdf")
        create_pdf(country, details, pdf_path)
