USE manufacturing;

CREATE TABLE defect_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    machine_id VARCHAR(50),
    defect_type VARCHAR(100),
    timestamp DATETIME,
    quantity INT
);

INSERT INTO defect_logs (machine_id, defect_type, timestamp, quantity)
VALUES
('M1', 'Alignment Issue', '2024-11-20 10:00:00', 5),
('M2', 'Overheating', '2024-11-20 11:00:00', 2),
('M1', 'Alignment Issue', '2024-11-21 09:00:00', 4),
('M3', 'Electrical Fault', '2024-11-21 15:00:00', 3),
('M3', 'Electrical Fault', '2024-11-24 16:00:00', 2),
('M2', 'Electrical Fault', '2024-11-24 16:00:00', 2),
('M3', 'Alignment Issue', '2024-11-24 06:00:00', 2),
('M1', 'Overheating', '2024-09-24 16:00:00', 2);
