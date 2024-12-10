import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
from sqlalchemy import create_engine
from statsmodels.tsa.arima.model import ARIMA


# Load defect data from MySQL
def load_data():
    # conn = mysql.connector.connect(
    #    host="localhost",
    #    user="root",
    #    password="12345678",
    #    database="manufacturing"
    # )

    # Create SQLAlchemy engine
    engine = create_engine(f"mysql+mysqlconnector://root:12345678@localhost/manufacturing")

    # query = "SELECT date, COUNT(*) as defect_count FROM defect_data GROUP BY date ORDER BY date;"
    query = "SELECT timestamp as date, COUNT(*) as defect_count FROM defect_logs GROUP BY timestamp ORDER BY timestamp;"
    # df = pd.read_sql(query, conn)
    # conn.close()

    # Read data into a Pandas DataFrame
    df = pd.read_sql(query, engine)
    return df


# Perform ARIMA forecasting
def forecast_defects(data):
    print("---  call forecast_defects")

    # Convert 'date' column to datetime and set as index
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)

    # Ensure data is sorted by date and set frequency
    data = data.sort_index().asfreq('D')  # Set frequency to daily ('D')

    # Handle missing values (if any)
    data['defect_count'] = data['defect_count'].fillna(0)

    # Fit ARIMA model (Ensure data is stationary if needed)
    model = ARIMA(data['defect_count'], order=(1, 1, 1))
    model_fit = model.fit()

    # Forecast for the next 30 days
    forecast = model_fit.forecast(steps=30)
    forecast_dates = pd.date_range(data.index[-1] + pd.Timedelta(days=1), periods=30, freq='D')

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['defect_count'], label='Historical Data', marker='o')
    plt.plot(forecast_dates, forecast, label='Forecast', marker='x', linestyle='--', color='red')
    plt.title('Defect Trend and Forecast')
    plt.xlabel('Date')
    plt.ylabel('Defect Count')
    plt.legend()
    plt.grid()
    plt.show()

    return forecast, forecast_dates


# Enhanced Report Function
def generate_report(data, forecast, forecast_dates):
    print("---  call generate_report")

    # Ensure the 'reports' folder exists
    os.makedirs("reports", exist_ok=True)

    # Ensure data is sorted by date and set frequency
    data = data.sort_index().asfreq('D')  # Set frequency to daily ('D')

    # Handle missing values (if any)
    data['defect_count'] = data['defect_count'].fillna(0)

    # Fit ARIMA model (Ensure data is stationary if needed)
    model = ARIMA(data['defect_count'], order=(1, 1, 1))
    model_fit = model.fit()

    # Forecast for the next 30 days
    forecast = model_fit.forecast(steps=30)
    forecast_dates = pd.date_range(data.index[-1] + pd.Timedelta(days=1), periods=30, freq='D')

    # Generate plot
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['defect_count'], label='Historical Data', marker='o')
    plt.plot(forecast_dates, forecast, label='Forecast', marker='x', linestyle='--', color='red')
    plt.title('Defect Trend and Forecast')
    plt.xlabel('Date')
    plt.ylabel('Defect Count')
    plt.legend()
    plt.grid()

    # File paths
    png_path = os.path.join("reports", "defect_report_chart.png")
    pdf_path = os.path.join("reports", "defect_report.pdf")

    # Save plot as PNG
    plt.savefig(png_path)
    plt.close()

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add title
    pdf.cell(200, 10, txt="Manufacturing Defect Analysis Report", ln=True, align='C')
    pdf.cell(200, 10, txt="Forecast Summary", ln=True, align='L')

    # Add forecast details
    pdf.ln(10)  # Add space
    for date, count in zip(forecast_dates, forecast):
        pdf.cell(200, 10, txt=f"{date.date()}: {int(count)} defects", ln=True, align='L')

    # Add chart image to the PDF
    pdf.image(png_path, x=10, y=pdf.get_y() + 10, w=180)

    # Save the PDF
    pdf.output(pdf_path)

    print(f"Report saved as PNG: {png_path}")
    print(f"Report saved as PDF: {pdf_path}")
    return forecast, forecast_dates


# Send email alert
def send_email_alert(forecast, forecast_dates, threshold=100):
    high_defect_dates = [(date, count) for date, count in zip(forecast_dates, forecast) if count > threshold]
    if not high_defect_dates:
        print("No alerts: Defects are within the safe threshold. No email sent out.")
        return

    # Email credentials
    sender_email = "dublin9582@gmail.com"
    receiver_email = "yuying6688@yahoo.com"
    password = "TarTan@2017"

    # Email content
    subject = "Manufacturing Defect Alert"
    body = "The following dates are forecasted to exceed the defect threshold:\n\n"
    body += "\n".join([f"{date.date()}: {int(count)} defects" for date, count in high_defect_dates])

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Add report as attachment
    # with open("defect_report.pdf", "rb") as attachment:
    with open(os.path.join("reports", "defect_report.pdf"), "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= defect_report.pdf")
        message.attach(part)

    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Alert email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Main workflow
if __name__ == "__main__":
    data = load_data()
    forecast, forecast_dates = forecast_defects(data)
    generate_report(data, forecast, forecast_dates)
    send_email_alert(forecast, forecast_dates)
