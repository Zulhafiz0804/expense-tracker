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
def add_expense(amount, category, description, date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
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
    print(f"✓ Expense added: ${amount} - {description}")

# View all expenses
def view_all_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    
    print("\n" + "="*60)
    print(f"{'ID':<5} {'Date':<12} {'Category':<12} {'Amount':<10} {'Description':<20}")
    print("="*60)
    for exp in expenses:
        print(f"{exp['id']:<5} {exp['date']:<12} {exp['category']:<12} ${exp['amount']:<9.2f} {exp['description']:<20}")
    print("="*60 + "\n")

# View spending by category
def view_by_category():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    
    category_totals = {}
    for exp in expenses:
        category = exp['category']
        category_totals[category] = category_totals.get(category, 0) + exp['amount']
    
    print("\n" + "="*40)
    print(f"{'Category':<20} {'Total':<10}")
    print("="*40)
    for category, total in sorted(category_totals.items()):
        print(f"{category:<20} ${total:<9.2f}")
    print("="*40 + "\n")

    # Delete an expense
def delete_expense():
    expenses = load_expenses()
    if not expenses:
        print("No expenses to delete.")
        return
    
    view_all_expenses()  # Show all expenses first
    
    try:
        expense_id = int(input("Enter the ID of the expense to delete: "))
        expenses = [exp for exp in expenses if exp['id'] != expense_id]
        save_expenses(expenses)
        print(f"✓ Expense {expense_id} deleted.")
    except ValueError:
        print("Invalid ID. Please enter a number.")

        # View expenses for a specific month
def view_by_month():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    
    month_input = input("Enter month (YYYY-MM, e.g., 2026-02): ").strip()
    
    month_expenses = [exp for exp in expenses if exp['date'].startswith(month_input)]
    
    if not month_expenses:
        print(f"No expenses found for {month_input}.")
        return
    
    total = sum(exp['amount'] for exp in month_expenses)
    
    print("\n" + "="*60)
    print(f"Expenses for {month_input}")
    print("="*60)
    print(f"{'ID':<5} {'Date':<12} {'Category':<12} {'Amount':<10} {'Description':<20}")
    print("="*60)
    for exp in month_expenses:
        print(f"{exp['id']:<5} {exp['date']:<12} {exp['category']:<12} ${exp['amount']:<9.2f} {exp['description']:<20}")
    print("="*60)
    print(f"Total for {month_input}: ${total:.2f}\n")

    # Set and check budget
def check_budget():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    
    month_input = input("Enter month to check budget (YYYY-MM, e.g., 2026-02): ").strip()
    budget = float(input("Enter your budget for this month: $"))
    
    month_expenses = [exp for exp in expenses if exp['date'].startswith(month_input)]
    total_spent = sum(exp['amount'] for exp in month_expenses)
    remaining = budget - total_spent
    
    print("\n" + "="*40)
    print(f"Budget Report for {month_input}")
    print("="*40)
    print(f"Budget:        ${budget:.2f}")
    print(f"Spent:         ${total_spent:.2f}")
    print(f"Remaining:     ${remaining:.2f}")
    
    if remaining < 0:
        print(f"⚠ OVER BUDGET by ${abs(remaining):.2f}")
    else:
        percentage = (total_spent / budget) * 100
        print(f"✓ {percentage:.1f}% of budget used")
    print("="*40 + "\n")

# Main menu
def main():
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. View by category")
        print("4. View by month")
        print("5. Check budget")
        print("6. Delete expense")
        print("7. Exit")
        
        choice = input("Choose an option (1-7): ").strip()
        
        if choice == "1":
            try:
                amount = float(input("Amount: $"))
                category = input("Category (food, transport, bills, entertainment, etc.): ").strip()
                description = input("Description: ").strip()
                add_expense(amount, category, description)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        
        elif choice == "2":
            view_all_expenses()
        
        elif choice == "3":
            view_by_category()
        
        elif choice == "4":
            view_by_month()
        
        elif choice == "5":
            check_budget()
        
        elif choice == "6":
            delete_expense()
        
        elif choice == "7":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()