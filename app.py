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

# ----------- Sidebar ------------------------------------
with st.sidebar:
    st.markdown("## 💰 Finance Analyzer")
    st.divider()

    st.markdown("### 📂 Upload Statements")
    uploaded_files = st.file_uploader(
        "Upload CSV bank statements",
        type=["csv"],
        accept_multiple_files=True,
        help="Upload one or more monthly CSV statements"
    )

    st.divider()

    st.markdown("### 🎯 Budget Settings")
    st.caption("Set monthly limits per category")

    # budget inputs for each category
    budgets = {
        "Food & Groceries": st.number_input("Food & Groceries", value=5000, step=500),
        "Transport":        st.number_input("Transport", value=3000, step=500),
        "Entertainment":    st.number_input("Entertainment", value=2000, step=500),
        "Utilities":        st.number_input("Utilities", value=3000, step=500),
        "Health":           st.number_input("Health", value=2000, step=500),
        "Education":        st.number_input("Education", value=2000, step=500),
        "Rent":             st.number_input("Rent", value=15000, step=1000),
        "Other":            st.number_input("Other", value=2000, step=500)
    }

    st.divider()

    st.markdown("### 💾 Savings Goal")
    savings_goal = st.number_input("Monthly savings target (KES)", value=5000, step=1000)


# ------- Main content ------------------------------------------------------
st.markdown("# 💰 Personal Finance Analyzer")
st.markdown("*AI-powered insights into your spending habits")

if not uploaded_files:
    st.markdown("""
    <div style='text-align: center; padding: 80px 0; color: #666'>
        <h2>👈 Upload your bank statements to get started </h2>
        <p>Supports CSV files with Date, Description, and Amount columns</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ---------- Load and combine all uploaded files -----------------------------------------
all_dfs = []
for file in uploaded_files:
    df = load_statement(file)
    df["Source"] = file.name
    all_dfs.append(df)

df = pd.concat(all_dfs, ignore_index=True)

# -------------- AI Categorization --------------------------
with st.spinner("Categorizing your transactions..."):
    descriptions = df["Description"].unique().tolist()
    categories = categorize_transactions(descriptions)
    df["Category"] = df["Description"].map(categories).fillna("Other")


# -------------- Summary metrics -----------------------------------------
summary = get_summary(df)

st.markdown('<p class="section-header"> Monthly Overview</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Income", f"KES {summary['total_income']:,.0f}")
with col2:
    st.metric("Total Expenses", f"KES {summary['total_expenses']:,.0f}")
with col3:
    delta = summary['net_savings'] - savings_goal
    st.metric(
        "Net Savings",
        f"KES {summary['net_savings']:,.0f}",
        delta=f"KES {delta:,.0f} vs goal",
        delta_color="normal" if delta >= 0 else "inverse"
    )
with col4:
    rate = (summary['net_savings'] / summary['total_income'] * 100) if summary['total_income'] > 0 else 0
    st.metric("Savings Rate", f"{rate:.1f}%")

st.divider()

# ----------------- Budget Tracker -------------------------------------------------
st.markdown('<p class="section-header"> Budget vs Actual</p>', unsafe_allow_html=True)

category_totals = df[df["Type"] == "Expense"].groupby("Category")["AbsAmount"].sum().to_dict()

cols = st.columns(4)
for i, (category, budget) in enumerate(budget.items()):
    actual = category_totals.get(category, 0)
    pct = (actual / budget * 100) if budget > 0 else 0
    over = actual > budget

    with cols[i % 4]:
        if over:
            st.markdown(f"""
            <div class="budget-warning">
                <strong>{category}</strong><br>
                KES {actual:,.0f} / {budget:,.0f}<br>
                <small>⚠️ {pct:.0f}% of budget used</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="budget-ok">
                <strong>{category}</strong><br>
                KES {actual:,.0f} / {budget:,.0f}<br>
                <small> {pct:.0f}% of budget used</small>
            </div>
            """, unsafe_allow_html=True)

st.divider()


# ------------------------- Charts ---------------------------------------------------------
st.markdown('<p class="section-header"> Spending Analysis</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(spending_by_category_chart(df), use_container_width=True)
with col2:
    st.plotly_chart(top_expenses_chart(df), use_container_width=True)

st.plotly_chart(spending_over_time_chart(df), use_container_width=True)

if len(uploaded_files) > 1:
    st.plotly_chart(monthly_comparison_chart(df), use_container_width=True)

st.divider()

# ------------------- Smart AI Insights ----------------------------------------------
st.markdown('<p class="section-header"> AI Insights</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 💡 Smart Observations")
    with st.spinner("Analyzing patterns..."):
        insights = get_smart_insights(df, category_totals, budgets)
    st.markdown(insights)

with col2:
    st.markdown("#### 🎯 Recommendations")
    with st.spinner("Generating recommendations..."):
        recommendations = get_recommendations(summary, category_totals)
    st.markdown(recommendations)

st.divider()


# --------------- PDF Export -------------------------------------------------------
st.markdown('<p class="section-header"> Export Report</p>', unsafe_allow_html=True)

if st.button("Generate PDF Report", use_container_width=True):
    with st.spinner("Generating your report..."):
        pdf_bytes = generate_pdf_report(summary, category_totals, budgets, savings_goal)
        st.download_button(
            label="⬇️ Download PDF Report",
            data=pdf_bytes,
            file_name="finance_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )


# ------------ Raw data ------------------------------------------------------------------
with st.expander("View raw transactions"):
    category_filter = st.selectbox("Filter by category", ["All"] + list(df["Category"].unique()))
    filtered = df if category_filter == "All" else df[df["Category"] == category_filter]
    st.dataframe(filtered[["Date", "Description", "Amount", "Category", "Type"]], use_container_width=True)