import os

import mysql.connector
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

# This script uses a simple regression model to predict defect types based on input parameters.

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


def train_predictive_model():
    data = fetch_data()
    print("Data Sample:\n", data.head())

    # Encode defect types
    data['DefectType'] = data['DefectType'].astype('category').cat.codes

    # Split into features and labels
    X = data[['Temperature', 'Humidity']]
    y = data['DefectType']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)

    print("\nClassification Report:\n", report)

    # Save the Classification report to a file
    report_path = os.path.join("reports", "predictive_model_report.txt")
    with open(report_path, "w") as file:
        file.write(report)

    print(f"\n ----> Classification report saved to {report_path}")

    # Feature importance
    feature_importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    print("\nFeature Importance:\n", feature_importance)

    # Construct the path to the reports folder
    resources_folder = os.path.join(os.getcwd(), 'reports')

    # Ensure the resources folder exists
    os.makedirs(resources_folder, exist_ok=True)

    # Path to save the Excel file
    output_file_path = os.path.join(resources_folder, 'feature_importance.xlsx')

    # Save feature importance to Excel file
    feature_importance.to_excel(output_file_path, index=True)
    print(f"\n----> Feature importance saved to {output_file_path}")


if __name__ == "__main__":
    train_predictive_model()
