from fpdf import FPDF
from datetime import datetime

def generate_pdf_report(summary: dict, category_totals: dict,
                        budgets: dict, savings_goal: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()

