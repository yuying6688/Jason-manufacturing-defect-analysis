import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
import xlsxwriter
import os
from flask import Flask, render_template

# Database connection
engine = create_engine('mysql+pymysql://root:12345678@localhost/defect_analysis')

# Load CSV data
# defects_df = pd.read_csv('defects.csv')

# Construct the path to the CSV file
file_path = os.path.join('../resources', 'defects.csv')

# Read the CSV file
defects_df = pd.read_csv(file_path)

# Delete all existing data from the defects table
with engine.begin() as connection:  # Begin a transaction
    connection.execute(text("DELETE FROM defects"))
print("\n =============> Data cleaned or deleted successfully! ===============")

# Save to MySQL
defects_df.to_sql('defects', con=engine, if_exists='append', index=False)
print("\n =============> Data imported successfully! ==============")

# Calculate defect frequency
frequency = defects_df['defect_type'].value_counts()
print("\n =============> Calculate Defect Frequency:\n", frequency)

# Visualization
# Create a bar chart of defect frequencies:
print("\n =============> Visualization Create a bar chart of defect frequencies ...............\n")
def plot_defect_frequency(data):
    data.plot(kind='bar', color='skyblue')
    plt.title('Defect Frequency')
    plt.xlabel('Defect Type')
    plt.ylabel('Count')
    plt.show()

plot_defect_frequency(frequency)


# Create a new Excel file and add a worksheet
# print("\n =============> Create a new Excel file and add a worksheet ...............\n")
# workbook = xlsxwriter.Workbook('Defect_Report.xlsx')
# worksheet = workbook.add_worksheet()

# Write data
# worksheet.write(0, 0, 'Defect Type')
# worksheet.write(0, 1, 'Frequency')
# row = 1
# for defect, count in frequency.items():
#     worksheet.write(row, 0, defect)
#     worksheet.write(row, 1, count)
#     row += 1

# workbook.close()
# print("\n =============> Report generated successfully!")


print("\n =============> Create a new Excel file and add a worksheet ...............\n")
# Query the defects table
query = """
SELECT defect_type AS `Defect Type`, 
       SUM(quantity) AS `Quantity`
FROM defects
GROUP BY defect_type
"""

# Load data into a DataFrame
defects_df = pd.read_sql(query, engine)

# Construct the path to the reports folder
resources_folder = os.path.join(os.getcwd(), '../reports')

# Ensure the resources folder exists
os.makedirs(resources_folder, exist_ok=True)

# Path to save the Excel file
output_file_path = os.path.join(resources_folder, 'Defect_Report.xlsx')

# Save the DataFrame to an Excel file
defects_df.to_excel(output_file_path, index=False)

print(f"Excel report saved to: {output_file_path}")
print("\n =============> Report generated successfully!")
