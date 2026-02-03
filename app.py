import streamlit as st
import json
import os
from datetime import datetime

# File to store expenses
EXPENSES_FILE = "expenses.json"

# Load expenses from file
def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'r') as f:
            return json.load(f)
    return []

# Save expenses to file
def save_expenses(expenses):
    with open(EXPENSES_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)

# Add a new expense
def add_expense(amount, category, description, date):
    expenses = load_expenses()
    expense = {
        "id": len(expenses) + 1,
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }
    expenses.append(expense)
    save_expenses(expenses)
    return True

# Page configuration
st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("💰 Expense Tracker")

# Sidebar for navigation
page = st.sidebar.radio("Choose a page:", 
    ["Add Expense", "View All", "By Category", "By Month", "Budget Check", "Delete Expense"])

# Page 1: Add Expense
if page == "Add Expense":
    st.header("➕ Add a New Expense")
    
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
        date = st.date_input("Date", value=datetime.now())
    
    with col2:
        category = st.selectbox("Category", 
            ["food", "transport", "bills", "entertainment", "shopping", "other"])
        description = st.text_input("Description")
    
    if st.button("✓ Add Expense", type="primary"):
        if amount > 0 and description:
            add_expense(amount, category, description, date.strftime("%Y-%m-%d"))
            st.success(f"Expense added: ${amount} - {description}")
        else:
            st.error("Please enter a valid amount and description.")

# Page 2: View All Expenses
elif page == "View All":
    st.header("📋 All Expenses")
    
    expenses = load_expenses()
    if expenses:
        # Convert to display format
        display_data = []
        for exp in expenses:
            display_data.append({
                "ID": exp['id'],
                "Date": exp['date'],
                "Category": exp['category'],
                "Amount": f"${exp['amount']:.2f}",
                "Description": exp['description']
            })
        
        st.dataframe(display_data, use_container_width=True)
        
        total = sum(exp['amount'] for exp in expenses)
        st.metric("Total Spent", f"${total:.2f}")
    else:
        st.info("No expenses recorded yet.")

# Page 3: View by Category
elif page == "By Category":
    st.header("📊 Spending by Category")
    
    expenses = load_expenses()
    if expenses:
        category_totals = {}
        for exp in expenses:
            category = exp['category']
            category_totals[category] = category_totals.get(category, 0) + exp['amount']
        
        # Display as table
        display_data = []
        for category, total in sorted(category_totals.items()):
            display_data.append({"Category": category, "Total": f"${total:.2f}"})
        
        st.dataframe(display_data, use_container_width=True)
        
        # Display as chart
        import pandas as pd
        df = pd.DataFrame(display_data)
        df['Total'] = df['Total'].str.replace('$', '').astype(float)
        st.bar_chart(df.set_index('Category'))
    else:
        st.info("No expenses recorded yet.")

# Page 4: View by Month
elif page == "By Month":
    st.header("📅 Expenses by Month")
    
    expenses = load_expenses()
    if expenses:
        month_input = st.text_input("Enter month (YYYY-MM, e.g., 2026-02)")
        
        if month_input:
            month_expenses = [exp for exp in expenses if exp['date'].startswith(month_input)]
            
            if month_expenses:
                display_data = []
                for exp in month_expenses:
                    display_data.append({
                        "ID": exp['id'],
                        "Date": exp['date'],
                        "Category": exp['category'],
                        "Amount": f"${exp['amount']:.2f}",
                        "Description": exp['description']
                    })
                
                st.dataframe(display_data, use_container_width=True)
                
                total = sum(exp['amount'] for exp in month_expenses)
                st.metric(f"Total for {month_input}", f"${total:.2f}")
            else:
                st.warning(f"No expenses found for {month_input}.")
    else:
        st.info("No expenses recorded yet.")

# Page 5: Budget Check
elif page == "Budget Check":
    st.header("💵 Budget Report")
    
    expenses = load_expenses()
    if expenses:
        col1, col2 = st.columns(2)
        
        with col1:
            month_input = st.text_input("Enter month (YYYY-MM, e.g., 2026-02)")
        
        with col2:
            budget = st.number_input("Budget for this month ($)", min_value=0.0, step=1.0)
        
        if month_input and budget > 0:
            month_expenses = [exp for exp in expenses if exp['date'].startswith(month_input)]
            total_spent = sum(exp['amount'] for exp in month_expenses)
            remaining = budget - total_spent
            percentage = (total_spent / budget) * 100 if budget > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Budget", f"${budget:.2f}")
            
            with col2:
                st.metric("Spent", f"${total_spent:.2f}")
            
            with col3:
                st.metric("Remaining", f"${remaining:.2f}")
            
            st.progress(min(percentage / 100, 1.0))
            
            if remaining < 0:
                st.error(f"⚠️ Over budget by ${abs(remaining):.2f}")
            else:
                st.success(f"✓ {percentage:.1f}% of budget used")
    else:
        st.info("No expenses recorded yet.")

# Page 6: Delete Expense
elif page == "Delete Expense":
    st.header("🗑️ Delete Expense")
    
    expenses = load_expenses()
    if expenses:
        # Create a list of expenses to select from
        expense_options = []
        for exp in expenses:
            option_text = f"ID {exp['id']}: ${exp['amount']:.2f} - {exp['description']} ({exp['date']})"
            expense_options.append((exp['id'], option_text))
        
        selected = st.selectbox("Select expense to delete:", 
            options=[opt[0] for opt in expense_options],
            format_func=lambda x: [opt[1] for opt in expense_options if opt[0] == x][0])
        
        if st.button("🗑️ Delete Selected Expense", type="primary"):
            expenses = [exp for exp in expenses if exp['id'] != selected]
            save_expenses(expenses)
            st.success(f"Expense {selected} deleted!")
            st.rerun()
    else:
        st.info("No expenses to delete.")