import json
import os
from datetime import datetime
from collections import defaultdict

class ExpenseTracker:
    def __init__(self, user_email):
        self.user_email = user_email
        self.expenses = []
        self.budgets = defaultdict(dict)

        if os.path.exists(f'{self.user_email}_data.json'):
            print(f"✔ Existing data file found for {self.user_email}. Loading data...")
        else:
            print(f"ℹ No previous data found for {self.user_email}. Starting fresh.")

        self.load_data()

    def load_data(self):
        try:
            with open(f'{self.user_email}_data.json', 'r') as f:
                data = json.load(f)
                self.expenses = data.get("expenses", [])
                self.budgets = defaultdict(dict, data.get("budgets", {}))
        except FileNotFoundError:
            pass

    def save_data(self):
        with open(f'{self.user_email}_data.json', 'w') as f:
            json.dump({
                "expenses": self.expenses,
                "budgets": self.budgets
            }, f, indent=2)

    def log_expense(self, amount, category, description=""):
        date = datetime.now().strftime('%Y-%m-%d')
        month = date[:7]
        
        self.expenses.append({
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        })
        
        self.save_data()
        self.check_budget_alert(month, category)

    def set_budget(self, month, category, amount):
        self.budgets[month][category] = amount
        self.save_data()

    def get_total_spending(self, month):
        return sum(
            e['amount'] 
            for e in self.expenses 
            if e['date'].startswith(month)
        )

    def get_spending_by_category(self, month):
        category_totals = defaultdict(float)
        for e in self.expenses:
            if e['date'].startswith(month):
                category_totals[e['category']] += e['amount']
        return category_totals

    def compare_budget(self, month):
        report = {}
        all_categories = set(self.budgets[month].keys()) | set(self.get_spending_by_category(month).keys())

        if not all_categories:
            return None

        spending = self.get_spending_by_category(month)

        for category in all_categories:
            spent = spending.get(category, 0.0)
            budget = self.budgets[month].get(category, 0.0)
            report[category] = {
                "spent": spent,
                "budget": budget,
                "remaining": budget - spent,
                "status": "Over Budget" if spent > budget else "Within Budget"
            }

        return report

    def check_budget_alert(self, month, category):
        budget = self.budgets[month].get(category, None)
        if budget is not None:
            spent = self.get_spending_by_category(month).get(category, 0)
            if spent > budget:
                print(f"[ALERT] You have exceeded your budget for {category} in {month}!")
            elif spent > 0.9 * budget:
                print(f"[WARNING] You're about to reach your budget for {category} in {month}!")

# --- Main Program ---
email = input("Enter your email: ")
tracker = ExpenseTracker(email)

while True:
    print("\n--- Expense Tracker Menu ---")
    print("1. Log Expense")
    print("2. Set Budget")
    print("3. View Total Monthly Spending")
    print("4. View Spending by Category")
    print("5. Compare Spending vs Budget")
    print("6. Exit")

    choice = input("Select an option (1-6): ")

    if choice == "1":
        amount = float(input("Enter amount: "))
        category = input("Enter category (e.g., Food, Transport): ")
        description = input("Enter description (optional): ")
        tracker.log_expense(amount, category, description)

    elif choice == "2":
        month = input("Enter month (YYYY-MM): ")
        category = input("Enter category: ")
        amount = float(input("Enter budget amount: "))
        tracker.set_budget(month, category, amount)

    elif choice == "3":
        month = input("Enter month (YYYY-MM): ")
        total = tracker.get_total_spending(month)
        print(f"Total spending in {month}: Rs.{total:.2f}/-")

    elif choice == "4":
        month = input("Enter month (YYYY-MM): ")
        spending = tracker.get_spending_by_category(month)
        if spending:
            print(f"Spending by category in {month}:")
            for cat, amt in spending.items():
                print(f"{cat}: Rs.{amt:.2f}/-")
        else:
            print(f"No spending data for {month}.")

    elif choice == "5":
        month = input("Enter month (YYYY-MM): ")
        report = tracker.compare_budget(month)
        if report:
            print(f"Budget report for {month}:")
            for cat, details in report.items():
                print(f"{cat}: Spent Rs.{details['spent']:.2f}/-, Budget Rs.{details['budget']:.2f}/-, "
                      f"Remaining Rs.{details['remaining']:.2f}/- - {details['status']}")
        else:
            print(f"No spending or budget data available for {month}.")

    elif choice == "6":
        print("Exiting. Thanks! for using the service")
        break

    else:
        print("Invalid option. Please try again.")
