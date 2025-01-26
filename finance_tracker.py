import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize or load data
def load_data(file_path="expenses.csv"):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])

def save_data(data, file_path="expenses.csv"):
    data.to_csv(file_path, index=False)

# Add an expense
def add_expense(data):
    date = input("Enter date (YYYY-MM-DD): ")
    amount = float(input("Enter amount: "))
    category = input("Enter category (e.g., Food, Rent, Entertainment): ")
    description = input("Enter description: ")
    new_expense = {"Date": date, "Amount": amount, "Category": category, "Description": description}
    data = data.append(new_expense, ignore_index=True)
    return data

# View spending summary
def view_summary(data):
    print("\nTotal Spending:", data["Amount"].sum())
    print("\nSpending by Category:")
    print(data.groupby("Category")["Amount"].sum())

# Plot spending trends
def plot_spending(data):
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values("Date")
    plt.plot(data["Date"], data["Amount"], marker="o")
    plt.title("Spending Over Time")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.grid()
    plt.show()

# Main menu
def main():
    file_path = "expenses.csv"
    data = load_data(file_path)

    while True:
        print("\n1. Add Expense")
        print("2. View Summary")
        print("3. Plot Spending Trends")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            data = add_expense(data)
            save_data(data, file_path)
        elif choice == "2":
            view_summary(data)
        elif choice == "3":
            plot_spending(data)
        elif choice == "4":
            save_data(data, file_path)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
