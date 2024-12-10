import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd
import seaborn as sns

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='manufacturing'
)

query = "SELECT * FROM defect_logs"
data = pd.read_sql(query, connection)
print("\n ========== Connect to the Database: ============")
print(data)

# Calculate Total Defects by Type:
print("\n ========== Analyze Defects - Calculate Total Defects by Type: ============")
defect_summary = data.groupby('defect_type')['quantity'].sum()
print(defect_summary)

# The reports Name: quantity, dtype:
# int64 is part of the default display of a Pandas Series.
# It shows the name of the series (in this case, the column name "quantity")
# and the data type (int64). This is expected behavior for Pandas.
#
# If you'd like to display the data without the extra metadata (like Name and dtype),
# you can customize the reports. Below are a few ways to handle this:
# Option 1: Convert to a Plain Dictionary

print(
    "\n ========== Analyze Defects Option 1: Convert to a Plain Dictionary on calculate Total Defects by Type: ============")
defect_summary_dict = defect_summary.to_dict()
print(defect_summary_dict)

# Option 2: Pretty Print with Custom Formatting
# Use Python's for loop to display key-value pairs in a readable format:
# Identify Patterns Over Time:
print(
    "\n ========== Analyze Defects Option 2: Pretty Print with Custom Formatting on calculate Total Defects by Type: ============")
for defect_type, quantity in defect_summary.items():
    print(f"{defect_type}: {quantity}")

# Option 3: Use reset_index to Convert to a DataFrame
# If you want a tabular reports (similar to SQL results), convert the Series back to a DataFrame:
print(
    "\n ========== Analyze Defects Option 3: Use reset_index to Convert to a DataFrame on calculate Total Defects by Type: ============")
defect_summary_df = defect_summary.reset_index()
print(defect_summary_df)

# Option 4: Suppress Name and Dtype (If Printing Directly)
# If you just want to suppress the extra metadata for direct Series printing:
print(
    "\n ========== Analyze Defects Option 4: Suppress Name and Dtype (If Printing Directly) on calculate Total Defects by Type: ============")
print(defect_summary.to_string())

print("\n ========== Analyze Defects - Identify Patterns Over Time: ============")
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp', inplace=True)
defect_trend = data.resample('D')['quantity'].sum()
print(defect_trend)

print("\n ========== Analyze Defects - Visualize Defects: ============")
sns.barplot(x=defect_summary.index, y=defect_summary.values)
plt.title("Defects by Type")
plt.show()
