import os
import random
import time

def simulate_real_time_monitoring():
    THRESHOLD_TEMP = 90.0
    THRESHOLD_HUMIDITY = 75.0
    log_file = "real_time_monitoring_log.txt"

    while True:
        # Simulate real-time sensor data
        temperature = round(random.uniform(50.0, 100.0), 2)
        humidity = round(random.uniform(30.0, 80.0), 2)

        # Check thresholds and log alerts

        report_path = os.path.join("reports", log_file)
        with open(report_path, "a") as log:

        # with open(log_file, "a") as log:
            if temperature > THRESHOLD_TEMP or humidity > THRESHOLD_HUMIDITY:
                alert = f"ALERT: High values detected! Temperature: {temperature}, Humidity: {humidity}"
                print(alert)
                log.write(alert + "\n")
            else:
                normal = f"Normal: Temperature: {temperature}, Humidity: {humidity}"
                print(normal)
                log.write(normal + "\n")

        # Wait before generating the next data point
        time.sleep(3)

if __name__ == "__main__":
    simulate_real_time_monitoring()
