import streamlit as st
import pandas as pd
from data_processor import load_statement, get_summary
from categorizer import categorize_transactions
from visualizer import (spending_by_category_chart, spending_over_time_chart,
                        top_expenses_chart, monthly_comparison_chart, budget_vs_actual_chart)
from recommender import get_recommendations, get_smart_insights
from report import generate_pdf_report

# ------------ Page config -------------------------------------------
st.set_page_config(
    page_title="Finance Analyzer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Custom CSS --------------------------------------
st.markdown("""
<style>
    /* main background */
    .stApp { background-color: #0f1117; }
    
    /* metric cards */
    [data-testid="metric-container"] {
        background-color: #1e2130;
        border: 1px solid #2d3250;
        border-radius: 12px;
        padding: 16px;
    }
    
    /* sidebar */
    [data-testid="stSidebar] {
        background-color: #1e2130;
        border-right: 1px solid #2d3250;
    }
    
    /* section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #a8b2d8;
        border-bottom: 1px solid #2d3250;
        padding-bottom: 8px;
        margin-bottom: 16px;
    }
    
    /* budget warning */
    .budget-warning {
        background-color: #3d1f1f;
        border-left: 4px solid #e74c3c;
        padding: 12px;
        border-radius: 4px;
        margin: 8px 0;
    }
    
    /* budget ok */
    .budget-ok {
        background-color: #1f3d2a;
        border-left: 4px solid #2ecc71;
        padding: 12px;
        border-radius: 4px;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)