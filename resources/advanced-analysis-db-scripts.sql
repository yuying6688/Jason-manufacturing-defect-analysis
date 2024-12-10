
-- Step 1: Create the `defect_analysis` Schema
CREATE SCHEMA IF NOT EXISTS defect_analysis;

-- Step 2: Use the `defect_analysis` Schema
USE defect_analysis;

-- Step 3: Create the `defects` Table
CREATE TABLE IF NOT EXISTS defects (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- Unique identifier for each defect
    product_id INT NOT NULL,                  -- Reference to the product ID
    defect_type VARCHAR(255) NOT NULL,        -- Type of the defect (e.g., "Scratches")
    quantity INT NOT NULL DEFAULT 0,          -- Number of defects of this type
    defect_date DATETIME NOT NULL,            -- Date and time of defect reporting
    severity_level VARCHAR(50) DEFAULT NULL,  -- Severity level of the defect (e.g., "Low", "High")
    description TEXT DEFAULT NULL             -- Optional description of the defect
);


-- Insert Sample Data
INSERT INTO defects (product_id, defect_type, quantity, defect_date, severity_level, description)
VALUES
    (101, 'Scratches', 15, '2024-12-01 10:30:00', 'Low', 'Minor scratches on surface'),
    (102, 'Cracks', 5, '2024-12-01 11:00:00', 'High', 'Cracks found near hinge'),
    (103, 'Discoloration', 10, '2024-12-01 12:15:00', 'Medium', 'Slight discoloration on panel'),
    (103, 'Discoloration', 12, '2025-12-02 12:15:00', 'Medium', 'Slight discoloration on side panel'),
    (101, 'Dents', 2, '2024-12-01 13:45:00', 'High', 'Dents on the bottom panel'),
    (104, 'Dents', 6, '2025-12-01 13:45:00', 'Low', 'Dents on the side panel');


