import streamlit as st
import pandas as pd
from data_processor import load_statement, get_summary
from categorizer import categorize_transactions
from visualizer import spending_by_category_chart, spending_over_time_chart,top_expenses_chart
from recommender import get_recommendations

st.set_page_config(page_title="Personal Finance Analyzer", layout="wide")
st.title("Personal Finance Analyzer")
st.write("Upload your bank statements and get AI-powered insights into your spending.")

uploaded_file = st.file_uploader("Upload your bank statement", type=["csv"])

if uploaded_file:
    df = load_statement(uploaded_file)
    summary = get_summary(df)

    # ---- Top metrics row ----------------------------------
    st.subheader("Monthly Summary")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Income", f"KES {summary['total_income']:,.0f}")
    with col2:
        st.metric("Total Expenses", f"KES {summary['total_expenses']:,.0f}")
    with col3:
        color = "normal" if summary['net_savings'] > 0 else "inverse"
        st.metric("Net Savings", f"KES {summary['net_savings']:,.0f}", delta_color=color)
    st.divider()

    # ------ AI Categorization ------------------------------
    st.subheader("Categorizing your transactions...")

    with st.spinner("AI is categorizing your transactions..."):
        descriptions = df["Description"].unique().tolist()
        categories = categorize_transactions(descriptions)
        df["Category"] = df["Description"].map(categories).fillna("Other")
    st.success(f"Categorized {len(descriptions)} unique transactions.")

    # -------------- Charts ------------------------------------
    st.subheader("Spending Analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(spending_by_category_chart(df), use_container_width=True)

    with col2:
        st.plotly_chart(top_expenses_chart(df), use_container_width=True)

    st.plotly_chart(spending_over_time_chart(df), use_container_width=True)

    st.divider()

    # ------------ AI Recommendations -------------------------
    st.subheader("AI Recommendations")

    with st.spinner("Generating personalized recommendations..."):
        category_totals = df[df["Type"] == "Expense"].groupby("Category")["AbsAmount"].sum().to_dict()
        recommendations = get_recommendations(summary, category_totals)
    st.markdown(recommendations)
    st.divider()

    # ------------ Raw Data ----------------------------------
    with st.expander("View raw transaction data"):
        st.dataframe(df, use_container_width=True)