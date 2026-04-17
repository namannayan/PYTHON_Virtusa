
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("Program Started...")
file_path = r"C:\Users\naman\Downloads\140.xlsx"
df = pd.read_excel(file_path)
print("Excel File Loaded Successfully.\n")
print("First 5 Rows:\n")
print(df.head())

print("\nColumns in Dataset:")
print(df.columns)
# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Remove fully empty rows
df.dropna(how='all', inplace=True)

# Convert Date
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
df.dropna(subset=['Date'], inplace=True)

# Convert Amount
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df.dropna(subset=['Amount'], inplace=True)

# Convert negative to positive
df['Amount'] = df['Amount'].abs()

# Fill missing text values
df['Transaction Details'] = df['Transaction Details'].fillna("No Description")
df['Tags'] = df['Tags'].fillna("No Tag")
df['Remarks'] = df['Remarks'].fillna("No Remark")

# 3. FEATURE ENGINEERING


df['Month'] = df['Date'].dt.month_name()
df['Day'] = df['Date'].dt.day
df['Weekday'] = df['Date'].dt.day_name()

def categorize(row):
    text = str(row['Transaction Details']).lower()
    tag = str(row['Tags']).lower()
    remark = str(row['Remarks']).lower()

    combined = text + " " + tag + " " + remark

    # Money Transfer
    if ('money sent' in combined or
        'sent money' in combined or
        'to bank' in combined or
        'upi transfer' in combined or
        'transfer' in combined):

        return 'Money Transfer'

    # Food
    elif ('zomato' in combined or
          'swiggy' in combined or
          'food' in combined):

        return 'Food'

    # Travel
    elif ('uber' in combined or
          'ola' in combined or
          'metro' in combined or
          'bus' in combined):

        return 'Travel'

    # Bills
    elif ('bill' in combined or
          'recharge' in combined or
          'electricity' in combined):

        return 'Bills'

    # Shopping
    elif ('amazon' in combined or
          'flipkart' in combined or
          'shopping' in combined):

        return 'Shopping'

    # Entertainment
    elif ('movie' in combined or
          'netflix' in combined):

        return 'Entertainment'

    else:
        return 'Others'

df['Category'] = df.apply(categorize, axis=1)

# 5. INSIGHTS
print("\n========== MONTHLY INSIGHTS ==========")

total_spend = df['Amount'].sum()
avg_spend = df['Amount'].mean()
max_spend = df['Amount'].max()

print("Total Spend:", round(total_spend, 2))
print("Average Transaction:", round(avg_spend, 2))
print("Highest Transaction:", round(max_spend, 2))

cat_spend = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)

print("\nCategory Wise Spending:\n")
print(cat_spend)

print("\nHighest Spending Category:", cat_spend.idxmax())

day_spend = df.groupby('Date')['Amount'].sum()
print("Highest Spending Day:", day_spend.idxmax().date())


sns.set(style="whitegrid")

print("\nShowing Charts... Close one graph to see next.")

# Pie Chart
plt.figure(figsize=(8,8))
cat_spend.plot(kind='pie', autopct='%1.1f%%')
plt.title("Category Wise Expense")
plt.ylabel("")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,5))
sns.barplot(x=cat_spend.index, y=cat_spend.values)
plt.title("Category Spend")
plt.xlabel("Category")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

daily = df.groupby('Date')['Amount'].sum()

plt.figure(figsize=(12,5))
plt.plot(daily.index, daily.values, marker='o')
plt.title("Daily Expense Trend")
plt.xlabel("Date")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Weekday Spend
weekday_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
weekday_spend = df.groupby('Weekday')['Amount'].sum().reindex(weekday_order)

plt.figure(figsize=(10,5))
sns.barplot(x=weekday_spend.index, y=weekday_spend.values)
plt.title("Weekday Wise Spending")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
money_transfer = cat_spend.get('Money Transfer', 0)

print("\n========== SMART SUGGESTIONS ==========")

print("Money Transfer Total:", money_transfer)

if money_transfer > total_spend * 0.25:
    print("Large amount sent as transfers this month.")

if cat_spend.get('Food',0) > total_spend * 0.30:
    print("High Food spending detected.")

if avg_spend > 500:
    print("Average transaction value is high.")

print("Maintain monthly budget.")
print("Track unnecessary expenses.")

