from fpdf import FPDF
from datetime import datetime

def generate_pdf_report(summary: dict, category_totals: dict,
                        budgets: dict, savings_goal: float) -> bytes:
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

    pdf.set_text_color(30, 33, 48)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Budget vs Actual", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 33, 48)
    pdf.cell(70, 8, "Category", fill=True)
    pdf.cell(40, 8, "Budget (KES)", fill=True, align="R")
    pdf.cell(40, 8, "Actual (KES)", fill=True, align="R")
    pdf.cell(40, 8, "Status", fill=True, align="C", ln=True)

    pdf.set_font("Helvetica", "", 10)
    for category, budget in budgets.items():
        actual = category_totals.get(category, 0)
        over = actual > budget
        status = "Over budget" if over else "On track"

        pdf.set_text_color(80, 80, 80)
        pdf.cell(70, 8, category)
        pdf.cell(40, 8, f"{budget:,.0f}", align="R")
        pdf.cell(40, 8, f"{actual:,.0f}", align="R")

        pdf.set_text_color(231, 76, 60) if over else pdf.set_text_color(46, 204, 113)
        pdf.cell(40, 8, status, align="C", ln=True)

    pdf.ln(6)

    pdf.set_text_color(30, 33, 48)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Savings Goal Progress", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    progress = max(0, min(summary['net_savings'] / savings_goal, 1.0)) if savings_goal > 0 else 0

    bar_width = 190
    filled = int(bar_width * progress)

    pdf.set_fill_color(220, 220, 220)
    pdf.rect(10, pdf.get_y(), bar_width, 8, "F")

    color = (46, 204, 113) if progress >= 1.0 else (124, 131, 253)
    pdf.set_fill_color(*color)
    pdf.rect(10, pdf.get_y(), filled, 8, "F")

    pdf.ln(12)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, f"Progress: {progress*100:.0f}% of KES {savings_goal:,.0f} goal", ln=True)

    return bytes(pdf.output())
