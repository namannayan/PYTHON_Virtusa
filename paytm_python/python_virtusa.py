import pandas as pd
import matplotlib.pyplot as plt
file_name = r"C:\Users\naman\OneDrive\Desktop\paytm_python\expenses.csv"
try:
    pd.read_csv(file_name)
except:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df.to_csv(file_name, index=False)

# Add Expense
def add_expense():
    date = input("Enter Date (YYYY-MM-DD): ")
    category = input("Enter Category: ")
    amount = float(input("Enter Amount: "))
    description = input("Enter Description: ")

    df = pd.read_csv(file_name)

    new_row = {
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Description": description
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(file_name, index=False)

    print("Expense Added Successfully!")

# Show Summary
def show_summary():
    df = pd.read_csv(file_name)

    if df.empty:
        print("No expenses found.")
        return

    print("\nTotal Expense:", df["Amount"].sum())
    print("Average Expense:", df["Amount"].mean())
    print("Highest Expense:", df["Amount"].max())

    print("\nCategory Wise Expense:")
    print(df.groupby("Category")["Amount"].sum())

# Pie Chart
def pie_chart():
    df = pd.read_csv(file_name)

    if df.empty:
        print("No expenses found.")
        return

    category_sum = df.groupby("Category")["Amount"].sum()

    plt.figure(figsize=(8,8))
    plt.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%')
    plt.title("Expense Distribution")
    plt.show()

# Category Wise Bar Graph
def bar_graph():
    df = pd.read_csv(file_name)

    if df.empty:
        print("No expenses found.")
        return

    category_sum = df.groupby("Category")["Amount"].sum()

    plt.figure(figsize=(10,6))
    category_sum.plot(kind="bar")
    plt.title("Category Wise Expense")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Highest Spending Category
def highest_spending_category():
    df = pd.read_csv(file_name)

    if df.empty:
        print("No expenses found.")
        return

    category_sum = df.groupby("Category")["Amount"].sum()

    print("Highest Spending Category:", category_sum.idxmax())
    print("Amount:", category_sum.max())

# Suggestions
def suggestions():
    df = pd.read_csv(file_name)

    if df.empty:
        print("No expenses found.")
        return

    category_sum = df.groupby("Category")["Amount"].sum()
    total = df["Amount"].sum()

    print("\n--- Smart Suggestions ---")

    for category, amount in category_sum.items():
        percent = (amount / total) * 100

        if category.lower() == "food" and percent > 30:
            print("Food spending is high. Try eating homemade food.")

        elif category.lower() == "travel" and percent > 20:
            print("Travel spending is high. Use public transport if possible.")

        elif category.lower() == "shopping" and percent > 20:
            print("Shopping spending is high. Avoid unnecessary purchases.")

        elif category.lower() == "bills" and percent > 25:
            print("Bills are high. Save electricity and water.")

    if total > 15000:
        print("Overall spending is high. Set a monthly budget.")
    else:
        print("Good job! Your expenses are under control.")

# Reset Data
def reset_data():
    confirm = input("Do you want to delete all expense data? (yes/no): ")

    if confirm.lower() == "yes":
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        df.to_csv(file_name, index=False)
        print("All Data Deleted Successfully!")
    else:
        print("Cancelled.")

# PAYTM CSV 
def import_paytm():
    
    path = input("Enter the full path of PayTM CSV file: ").strip()
    path = path.strip('"').strip("'")   

    try:
        df_paytm = pd.read_csv(path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    
    required_cols = ["Date", "Tags", "Amount", "Transaction Details"]
    missing = [col for col in required_cols if col not in df_paytm.columns]
    if missing:
        print(f"Missing required columns: {missing}")
        print("Found columns:", list(df_paytm.columns))
        return

    df_clean = df_paytm[required_cols].copy()
    
    # Rename columns
    df_clean.rename(columns={
        "Tags": "Category",
        "Transaction Details": "Description"
    }, inplace=True)

    # Remove leading non-alphabetic characters (emoji, symbols) from Category
    df_clean["Category"] = df_clean["Category"].astype(str).str.replace(r'^[^A-Za-z]+', '', regex=True).str.strip()
    
    # Convert Amount to numeric (coerce errors to NaN)
    df_clean["Amount"] = pd.to_numeric(df_clean["Amount"], errors="coerce")
    # Drop rows where Amount is NaN or zero
    df_clean = df_clean.dropna(subset=["Amount"])
    df_clean = df_clean[df_clean["Amount"] != 0]

    # Make amounts positive .
    df_clean["Amount"] = df_clean["Amount"].abs()

    # Convert Date column to standard YYYY-MM-DD format
    try:
        df_clean["Date"] = pd.to_datetime(df_clean["Date"]).dt.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Date conversion error: {e}")
        print("Please ensure Date column contains valid dates.")
        return

    # Overwrite the expenses.csv file with this new data
    df_clean.to_csv(file_name, index=False)
    print(f"Successfully imported {len(df_clean)} expense records from PayTM.")
    print("expenses.csv has been replaced with the imported data.")

# Menu
def menu():
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. Show Summary")
        print("3. Pie Chart")
        print("4. Category Wise Bar Graph")
        print("5. Highest Spending Category")
        print("6. Smart Suggestions")
        print("7. Reset All Data")
        print("8. Import PayTM CSV")
        print("9. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            show_summary()
        elif choice == '3':
            pie_chart()
        elif choice == '4':
            bar_graph()
        elif choice == '5':
            highest_spending_category()
        elif choice == '6':
            suggestions()
        elif choice == '7':
            reset_data()
        elif choice == '8':
            import_paytm()
        elif choice == '9':
            print("Thank You!")
            break
        else:
            print("Invalid Choice")

menu()