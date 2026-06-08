import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"
CATEGORIES = ["Food", "Transport", "Entertainment", "Other"]


# File I/O 

def load_expenses():
    """Load expenses from the JSON data file. Returns an empty list if file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_expenses(expenses):
    """Save the expenses list to the JSON data file."""
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


# Core Features 

def add_expense(expenses):
    """Prompt the user for expense details and append to the list."""
    print("\n─── Add Expense ───────────────────────────────")

    # Amount
    while True:
        try:
            amount = float(input("Amount (₹): ").strip())
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    # Category
    print("Categories: " + " | ".join(f"{i+1}. {c}" for i, c in enumerate(CATEGORIES)))
    while True:
        choice = input("Choose category (1-4): ").strip()
        if choice in [str(i + 1) for i in range(len(CATEGORIES))]:
            category = CATEGORIES[int(choice) - 1]
            break
        print("Invalid choice. Enter a number between 1 and 4.")

    # Optional note
    note = input("Note (optional, press Enter to skip): ").strip()

    expense = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "category": category,
        "amount": amount,
        "note": note if note else "—"
    }

    expenses.append(expense)
    save_expenses(expenses)
    print(f"\n✓ Expense of ₹{amount:.2f} ({category}) saved.")


def print_table(expenses):
    """Print a formatted table of the given expenses list."""
    if not expenses:
        print("\n  No expenses to show.")
        return

    col_widths = {"date": 16, "category": 15, "amount": 10, "note": 30}
    header = (
        f"{'Date':<{col_widths['date']}}"
        f"{'Category':<{col_widths['category']}}"
        f"{'Amount':>{col_widths['amount']}}"
        f"  {'Note':<{col_widths['note']}}"
    )
    divider = "─" * len(header)

    print(f"\n{divider}")
    print(header)
    print(divider)

    for e in expenses:
        print(
            f"{e['date']:<{col_widths['date']}}"
            f"{e['category']:<{col_widths['category']}}"
            f"₹{e['amount']:>{col_widths['amount'] - 1}.2f}"
            f"  {e['note']:<{col_widths['note']}}"
        )

    total = sum(e["amount"] for e in expenses)
    print(divider)
    print(f"{'TOTAL':<{col_widths['date'] + col_widths['category']}}₹{total:>{col_widths['amount'] - 1}.2f}")
    print(divider)


def view_all_expenses(expenses):
    """Display every expense in a formatted table."""
    print("\n─── All Expenses ──────────────────────────────")
    print_table(expenses)


def filter_by_category(expenses):
    """Let the user pick a category and display only those expenses."""
    print("\n─── Filter by Category ────────────────────────")
    print("Categories: " + " | ".join(f"{i+1}. {c}" for i, c in enumerate(CATEGORIES)))

    while True:
        choice = input("Choose category (1-4): ").strip()
        if choice in [str(i + 1) for i in range(len(CATEGORIES))]:
            category = CATEGORIES[int(choice) - 1]
            break
        print("Invalid choice. Enter a number between 1 and 4.")

    filtered = [e for e in expenses if e["category"] == category]
    print(f"\n  Showing: {category}")
    print_table(filtered)


# Menu

def show_menu():
    """Print the main menu."""
    print("\n╔══════════════════════════════════╗")
    print("║    💰  Expense Tracker  💰        ║")
    print("╠══════════════════════════════════╣")
    print("║  1. Add expense                  ║")
    print("║  2. View all expenses            ║")
    print("║  3. Filter by category           ║")
    print("║  4. Exit                         ║")
    print("╚══════════════════════════════════╝")


def main():
    """Main loop — load data, show menu, dispatch to features."""
    expenses = load_expenses()

    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_all_expenses(expenses)
        elif choice == "3":
            filter_by_category(expenses)
        elif choice == "4":
            print("\nBye! Keep tracking 👋\n")
            break
        else:
            print("Invalid option. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
