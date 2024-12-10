-- Create the database
CREATE DATABASE IF NOT EXISTS advanced_defect_analysis;

USE advanced_defect_analysis;

-- Table to store manufacturing parameters
CREATE TABLE parameters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parameter_name VARCHAR(255) NOT NULL,
    parameter_value VARCHAR(255) NOT NULL
);

-- Table to store defect records
CREATE TABLE defects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    defect_type VARCHAR(255) NOT NULL,
    parameter_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parameter_id) REFERENCES parameters(id)
);

-- Table to store combined defect data for predictive modeling
CREATE TABLE defect_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parameter_value1 FLOAT NOT NULL,
    parameter_value2 FLOAT NOT NULL,
    defect_type VARCHAR(255) NOT NULL
);

-- Insert Sample Data
-- Realistic Test Data
-- Parameters include temperature, humidity, and pressure.
-- Defects include cracks, discoloration, and size variance.
-- Insert sample manufacturing parameters
INSERT INTO parameters (parameter_name, parameter_value)
VALUES
    ('Temperature', 'High'),
    ('Temperature', 'Low'),
    ('Humidity', 'High'),
    ('Humidity', 'Low'),
    ('Pressure', 'High'),
    ('Pressure', 'Low');

-- Insert sample defect records
INSERT INTO defects (defect_type, parameter_id)
VALUES
    ('Crack', 1),  -- High temperature
    ('Discoloration', 3),  -- High humidity
    ('Size Variance', 5),  -- High pressure
    ('Crack', 2),  -- Low temperature
    ('Discoloration', 4),  -- Low humidity
    ('Size Variance', 6);  -- Low pressure

-- Insert sample data for predictive modeling
INSERT INTO defect_data (parameter_value1, parameter_value2, defect_type)
VALUES
    (75.5, 55.3, 'Crack'),
    (60.2, 50.1, 'Discoloration'),
    (90.8, 70.5, 'Size Variance'),
    (70.0, 52.0, 'Crack'),
    (62.5, 48.8, 'Discoloration'),
    (95.2, 72.0, 'Size Variance');
