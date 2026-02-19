import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def send_otp_email(to_email, otp):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify Your Email - Cheap Flight Destination"
    message["From"] = EMAIL_USER
    message["To"] = to_email

    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 8px; text-align: center;">
                
                <h2 style="color: #2c3e50;">Email OTP</h2>
                <hr>

                <p>Dear User,</p>

                <p>Your One-Time Password (OTP) is:</p>

                <h1 style="color: #28a745; letter-spacing: 5px;">{otp}</h1>

                <p>Please use this OTP to complete your registration process.</p>
                <p style="color: red;">Do not share this code with anyone.</p>

                <p>Thank you for using <strong>Cheap Flight Destination ✈️</strong></p>

                <hr>
                <p style="font-size: 12px; color: gray;">
                    © 2026 Cheap Flight Destination. All rights reserved.
                </p>
            </div>
        </body>
    </html>
    """

    part = MIMEText(html_content, "html")
    message.attach(part)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(message)
    server.quit()
