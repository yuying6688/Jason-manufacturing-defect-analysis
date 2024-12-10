import pymysql
from sqlalchemy import create_engine
import pandas as pd
from scipy.stats import chi2_contingency
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import time

# from SimpleDefectAnalysis import connection  !!!!!!!

# Create SQLAlchemy engine
engine = create_engine("mysql+pymysql://root:12345678@localhost/advanced_defect_analysis")

print(" =======>  Feature 1: Identify patterns and correlations between defects and manufacturing parameters\n")
query = """
SELECT defect_type, parameter_name, parameter_value
FROM defects JOIN parameters
ON defects.parameter_id = parameters.id;
"""
# Use the engine with pandas
data = pd.read_sql(query, engine)

# Cross-tabulation of defect types and parameter values
contingency_table = pd.crosstab(data['defect_type'], data['parameter_value'])

# Chi-square test for independence
chi2, p, dof, expected = chi2_contingency(contingency_table)

print("  \n chi2 = " , chi2)
print("  p = " , p)
print("  dof = " , dof)
print("  expected = \n" , expected)

if p < 0.05:
    print("Significant correlation found between defect type and parameter value.\n")
else:
    print("No significant correlation found.\n")


print(" =======>  Feature 2: Predict potential defects based on input parameters using a simple machine learning model\n")
# Load data
query = """
SELECT parameter_value1, parameter_value2, defect_type
FROM defect_data;
"""
data = pd.read_sql(query, engine.connect())

X = data[['parameter_value1', 'parameter_value2']]  # Features
y = data['defect_type']  # Target

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print(f" Evaluation ----> Model accuracy: {accuracy_score(y_test, y_pred)}\n")

# Save model for reuse
with open('defect_predictor.pkl', 'wb') as file:
    pickle.dump(model, file)
print(f" =======> Save model for reuse ----> defect_predictor.pkl\n")


print(" =======>  Feature 3: Real-Time Monitoring Fetch live data and display defect trends.\n")
def fetch_real_time_data():
    engine = create_engine("mysql+pymysql://root:12345678@localhost/advanced_defect_analysis")

    # Establish connection
    connection = engine.connect()
    query = "SELECT * FROM defects ORDER BY timestamp DESC LIMIT 10;"
    while True:
        data = pd.read_sql(query, connection)
        print("\n****** Recent Defects:")
        print(data)
        time.sleep(10)  # Refresh every 10 seconds
    connection.close()

fetch_real_time_data()