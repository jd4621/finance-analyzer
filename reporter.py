from fpdf import FPDF
from datetime import datetime

def generate_pdf_report(summary: dict, category_totals: dict,
                        budgets: dict, savings_goal: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()

    pdf.set_fill_color(30, 33, 48)
    pdf.rect(0, 0, 210, 40, "F")

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(12)
    pdf.cell(0, 10, "Personal Finance Report", align="C")

    pdf.set_font("Helvetica", "", 10)
    pdf.set_y(26)
    pdf.cell(0, 6, f"Generated on {datetime.now().strftime('%B %d, %Y')}", align="C")

    pdf.ln(20)


    pdf.set_text_color(30, 33, 48)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Financial Summary", ln=True)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    metrics = [
        ("Total Income",    f"KES {summary['total_income']:,.0f}",      (46, 204, 113)),
        ("Total Expenses",  f"KES {summary['total_expenses']:,.0f}",    (231, 76, 60)),
        ("Net Savings",     f"KES {summary['net_savings']:,.0f}",
         (46, 204, 113) if summary['net_savings'] >= 0 else (231, 76, 60)),
        ("Savings Goal",    f"KES {savings_goal:,.0f}",                 (124, 131, 253)),
    ]

    for label, value, color in metrics:
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(80, 10, label)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*color)
        pdf.cell(80, 10, value, ln=True)

    pdf.ln(6)

