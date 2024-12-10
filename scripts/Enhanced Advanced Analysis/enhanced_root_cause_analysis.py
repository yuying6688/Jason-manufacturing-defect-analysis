import os

import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd

# MySQL connection setup
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "12345678",
    "database": "advanced_defect_analysis"
}


def fetch_data():
    conn = mysql.connector.connect(**db_config)
    query = """
    SELECT defect_data.parameter_value1 AS Temperature,
           defect_data.parameter_value2 AS Humidity,
           defect_data.defect_type AS DefectType
    FROM defect_data;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def perform_root_cause_analysis():
    data = fetch_data()
    print("Data Sample:\n", data.head())

    # Group by defect type and calculate mean values
    analysis = data.groupby("DefectType").mean()
    print("\nRoot Cause Analysis Results:\n", analysis)

    # Export to CSV
    # analysis.to_csv("root_cause_analysis.csv", index=True)
    # print("===> Results exported to root_cause_analysis.csv\n")

    # Construct the path to the reports folder
    resources_folder = os.path.join(os.getcwd(), 'reports')

    # Ensure the resources folder exists
    os.makedirs(resources_folder, exist_ok=True)

    # Path to save the Excel file
    output_file_path = os.path.join(resources_folder, 'root_cause_analysis.csv')

    # Save the DataFrame to a csv file
    analysis.to_csv(output_file_path, index=False)
    print("\n===> Results exported to root_cause_analysis.csv\n")

    # Plotting
    analysis.plot(kind="bar", figsize=(8, 6), title="Average Parameter Values by Defect Type")
    plt.xlabel("Defect Type")
    plt.ylabel("Average Value")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    perform_root_cause_analysis()
