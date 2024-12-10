import random

import mysql.connector
from faker import Faker

# MySQL connection setup
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "12345678",
    "database": "advanced_defect_analysis"
}

# Connect to MySQL
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Connected to the database successfully.")

    cursor.execute("DELETE FROM defect_data;")
    # Reset AUTO_INCREMENT to 1
    cursor.execute("ALTER TABLE defect_data AUTO_INCREMENT = 1;")
    print("AUTO_INCREMENT reset for defect_data table.")
    print(".............Table defects has been emptied.")
    conn.commit()

    cursor.execute("DELETE FROM defects;")
    # Reset AUTO_INCREMENT to 1
    cursor.execute("ALTER TABLE defects AUTO_INCREMENT = 1;")
    print("AUTO_INCREMENT reset for defects table.")
    print(".............Table defect_data has been emptied.")
    conn.commit()

    cursor.execute("DELETE FROM parameters;")
    # Reset AUTO_INCREMENT to 1
    cursor.execute("ALTER TABLE parameters AUTO_INCREMENT = 1;")
    print("AUTO_INCREMENT reset for parameters table.")
    print("............ Table parameters has been emptied.")
    conn.commit()

    # Truncate table parameters
    # cursor.execute("TRUNCATE TABLE parameters;")

    # Truncate table defect_data
    # cursor.execute("TRUNCATE TABLE defect_data;")

    # Truncate table defects
    # cursor.execute("TRUNCATE TABLE defects;")

    # Commit the changes (not strictly necessary for TRUNCATE, but a good practice)
    conn.commit()
    print("All tables have been emptied.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

# Faker instance for generating random data
faker = Faker()


# Generate and insert data
def generate_parameters():
    parameters = ["Temperature", "Humidity", "Pressure"]
    values = ["High", "Low"]
    for parameter in parameters:
        for value in values:
            cursor.execute("INSERT INTO parameters (parameter_name, parameter_value) VALUES (%s, %s)",
                           (parameter, value))
    conn.commit()
    print("Parameters inserted.")


def generate_defect_data(num_records=50):
    for _ in range(num_records):
        parameter_value1 = round(random.uniform(50.0, 100.0), 2)  # Simulate temperature or pressure
        parameter_value2 = round(random.uniform(30.0, 80.0), 2)  # Simulate humidity
        defect_type = random.choice(["Crack", "Discoloration", "Size Variance"])
        cursor.execute(
            "INSERT INTO defect_data (parameter_value1, parameter_value2, defect_type) VALUES (%s, %s, %s)",
            (parameter_value1, parameter_value2, defect_type)
        )
    conn.commit()
    print(f"{num_records} defect_data records inserted.")


def generate_defects(num_records=20):
    for _ in range(num_records):
        defect_types = ["Crack", "Discoloration", "Size Variance"]
        parameter_id = random.randint(1, 6)  # Assuming 6 parameter entries
        defect_type = random.choice(defect_types)
        cursor.execute("INSERT INTO defects (defect_type, parameter_id) VALUES (%s, %s)", (defect_type, parameter_id))
    conn.commit()
    print(f"{num_records} defect records inserted.")


# Main execution
def main():
    try:
        generate_parameters()
        generate_defects(num_records=20)  # Customize the number of defects
        generate_defect_data(num_records=50)  # Customize defect data count
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
