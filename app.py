import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import base64

# Set page config
st.set_page_config(page_title="FinAura - Smart Finance Tracker", layout="wide")

# Custom CSS for fonts and background
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;600&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Montserrat', sans-serif;
            background: linear-gradient(135deg, #f0f4f8, #d9e4f5);
            color: #1e1e1e;
        }
        .main .block-container {
            padding: 2rem 3rem;
        }
        .sidebar .sidebar-content {
            background: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar with logo and menu
with st.sidebar:
    st.image("finance.png", use_container_width=True)
    selected = option_menu("Navigation", ["Home", "Add Income", "Add Expense", "Income", "Expenses", "Reports", "Download Report"],
                           icons=['house', 'plus-circle', 'dash-circle', 'wallet2', 'cart4', 'bar-chart-line', 'download'],
                           menu_icon="grid-fill", default_index=0)

# Data storage (session state)
if "data" not in st.session_state:
    @st.cache_data
    def load_data():
        df = pd.DataFrame({
            "Date": pd.date_range(start="2024-01-01", periods=10, freq='M'),
            "Category": ["Salary", "Investment", "Groceries", "Rent", "Utilities"]*2,
            "Amount": [3000, 1500, 400, 1200, 250, 3200, 1600, 450, 1300, 300],
            "Type": ["Income", "Income", "Expense", "Expense", "Expense"]*2
        })
        df["Date"] = pd.to_datetime(df["Date"])
        return df

    st.session_state.data = load_data()

data = st.session_state.data

# Home Page
if selected == "Home":
    st.title("💰 Welcome to FinAura")
    st.subheader("Track your income, expenses, and financial health with ease.")
    st.markdown("""
    ### What you can do here:
    - Log your income and expenses
    - Visualize spending trends
    - Generate downloadable reports
    - Enjoy a modern and intuitive UI
    """)

# Add Income
elif selected == "Add Income":
    st.header("➕ Add New Income")
    with st.form("income_form"):
        date = st.date_input("Date")
        category = st.text_input("Category")
        amount = st.number_input("Amount", min_value=0.0)
        submit = st.form_submit_button("Add Income")

    if submit:
        new_row = {"Date": pd.to_datetime(date), "Category": category, "Amount": amount, "Type": "Income"}
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Income added successfully!")

# Add Expense
elif selected == "Add Expense":
    st.header("➖ Add New Expense")
    with st.form("expense_form"):
        date = st.date_input("Date")
        category = st.text_input("Category")
        amount = st.number_input("Amount", min_value=0.0)
        submit = st.form_submit_button("Add Expense")

    if submit:
        new_row = {"Date": pd.to_datetime(date), "Category": category, "Amount": amount, "Type": "Expense"}
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Expense added successfully!")

# Income Section
elif selected == "Income":
    st.header("💵 Income Overview")
    income_data = data[data['Type'] == 'Income']
    income_data["Date"] = pd.to_datetime(income_data["Date"])
    st.dataframe(income_data)
    total_income = income_data['Amount'].sum()
    st.metric("Total Income", f"$ {total_income:,.2f}")
    fig = px.bar(income_data, x='Date', y='Amount', color='Category', title="Income by Category")
    st.plotly_chart(fig, use_container_width=True)

# Expenses Section
elif selected == "Expenses":
    st.header("🧾 Expense Overview")
    expense_data = data[data['Type'] == 'Expense']
    expense_data["Date"] = pd.to_datetime(expense_data["Date"])
    st.dataframe(expense_data)
    total_expense = expense_data['Amount'].sum()
    st.metric("Total Expenses", f"$ {total_expense:,.2f}")
    fig = px.pie(expense_data, names='Category', values='Amount', title="Expense Distribution")
    st.plotly_chart(fig, use_container_width=True)

# Reports Section
elif selected == "Reports":
    st.header("📊 Financial Summary Report")
    summary = data.groupby(['Type', 'Category']).agg(Total_Amount=('Amount', 'sum')).reset_index()
    st.dataframe(summary)

    # Graph
    fig = px.bar(summary, x='Category', y='Total_Amount', color='Type', barmode='group',
                 title="Income vs Expenses by Category")
    st.plotly_chart(fig, use_container_width=True)

# Download Section
elif selected == "Download Report":
    st.header("📥 Download Your Report")
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Complete Report as CSV",
        data=csv,
        file_name='finaura_report.csv',
        mime='text/csv',
    )

    st.markdown("""
    ### 💡 Tip:
    You can analyze this CSV file in Excel or Google Sheets for deeper financial insights.
    """)








