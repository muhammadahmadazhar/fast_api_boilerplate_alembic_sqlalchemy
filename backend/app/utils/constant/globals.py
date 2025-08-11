import os
import random
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import selectinload
# import boto3
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

# s3 = boto3.client(
#     "s3",
#     aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#     aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
#     region_name=os.getenv("AWS_REGION"),
# )
# BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")


def generate_signed_url(file_key: str, expires_in: int = 3600) -> str:
    try:
        return s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": BUCKET_NAME, "Key": file_key},
            ExpiresIn=expires_in,
        )
    except Exception as e:
        print(f"Error generating signed URL: {e}")
        return ""


# def serialize_with_signed_attachments(items):
#     return [
#         {
#             **{k: v for k, v in vars(item).items() if not k.startswith("_")},
#             "attachments": [
#                 {
#                     **{k: v for k, v in vars(att).items() if not k.startswith("_")},
#                     "file_url": generate_signed_url(att.file_url),  # Replacing file_url
#                 }
#                 for att in getattr(item, "attachments", [])
#                 if att.file_url
#             ],
#         }
#         for item in items
#     ]


class UserRole(str, Enum):
    User = "user"
    ADMIN = "admin"


def format_time(time_str):
    if not time_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        return dt.strftime("%I:%M %p")
    except Exception:
        return time_str


def generate_otp():
    return str(random.randint(100000, 999999))


def years_since(timestamp: str) -> int:
    try:
        year = int(timestamp)
        current = datetime.today().year
        return current - year
    except:
        date_obj = datetime.fromisoformat(timestamp)
        current_date = datetime.now()
        years_diff = (current_date - date_obj).days // 365
        return years_diff


SENDER_EMAIL = os.getenv("USER_EMAIL")
SENDER_PASSWORD = os.getenv("USER_PASSWORD")

PRIMARY_COLOR = "#00A8A8"
TEXT_COLOR = "#09090B"
BG_COLOR = "#E7EBF0"
BUTTON_COLOR = "#00A8A8"
BUTTON_TEXT_COLOR = "#FFFFFF"
FONT_FAMILY = "Inter, sans-serif"


def send_email(email: str, subject: str, html_content: str):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP("smtpout.secureserver.net", 587) as server:
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
            print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)


def send_email_otp(email: str, otp: str):
    subject = "Your One-Time Password (OTP) for Creative Arts Connect"
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: {FONT_FAMILY};
                margin: 0;
                padding: 0;
                background-color: {BG_COLOR};
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background: #FFFFFF;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .logo {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .logo img {{
                width: 150px;
                height: auto;
            }}
            .content {{
                color: {TEXT_COLOR};
                font-size: 16px;
                line-height: 1.5;
            }}
            .otp-box {{
                background-color: {BG_COLOR};
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                margin: 20px 0;
            }}
            .otp-code {{
                font-size: 32px;
                font-weight: bold;
                color: {PRIMARY_COLOR};
                letter-spacing: 4px;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 14px;
                color: #707070;
                text-align: center;
            }}
            .support {{
                color: {PRIMARY_COLOR};
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">
                <img src="https://creativeartsconnect.com/wp-content/uploads/2024/12/Untitled-design.png" alt="Creative Arts Connect Logo">
            </div>
            <div class="content">
                <p>Dear User,</p>
                <p>Your One-Time Password (OTP) for verification is:</p>
                <div class="otp-box">
                    <div class="otp-code">{otp}</div>
                </div>
                <p>This OTP is valid for <strong>60 minutes</strong>. Please do not share this code with anyone.</p>
                <p>If you did not request this OTP, please ignore this email or contact our support team immediately.</p>
                <div class="footer">
                    <p>For assistance, reach out to us at <a href="mailto:support@creativeartsconnect.com" class="support">support@creativeartsconnect.com</a></p>
                    <p>Best regards,<br>Our team at Creative Arts Connect<br>www.creativeartsconnect.com</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    send_email(email, subject, html_content)


def send_email_reset_link(email: str, link: str):
    subject = "Reset Your Password - Creative Arts Connect"
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Inter', sans-serif;
                background-color: #E7EBF0; /* Light gray background */
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            .container {{
                max-width: 500px;
                background: #FFFFFF;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
                margin: 50px auto;
            }}
            .header {{
                font-size: 22px;
                color: #00A8A8; /* Primary Color */
                font-weight: bold;
                margin-bottom: 20px;
            }}
            .text {{
                font-size: 16px;
                color: #09090B; /* Text Color */
                margin-bottom: 20px;
            }}
            .button {{
                background-color: #00A8A8; /* Primary Color */
                color: #FFFFFF;
                padding: 12px 20px;
                text-decoration: none;
                font-weight: bold;
                border-radius: 5px;
                display: inline-block;
                font-size: 16px;
                margin-top: 10px;
            }}
            .button:hover {{
                background-color: #008B8B;
            }}
            .footer {{
                font-size: 12px;
                color: #707070; /* Secondary Text Color */
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">Reset Your Password</div>
            <p class="text">Click the button below to reset your password:</p>
            <a href="{link}" class="button">Reset Password</a>
            <p class="footer">If you did not request a password reset, you can ignore this email.</p>
        </div>
    </body>
    </html>
    """
    send_email(email, subject, html_content)


def send_invite_email(email: str, invite_link: str, therapist_name: str = "Therapist"):
    subject = "Join Our Creative Arts Connect Therapist Directory – Expand Your Reach!"
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: {FONT_FAMILY}, Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: {BG_COLOR};
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background: #FFFFFF;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .logo {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .logo img {{
                width: 150px;
                height: auto;
            }}
            .content {{
                color: {TEXT_COLOR};
                font-size: 16px;
                line-height: 1.6;
            }}
            .benefits {{
                margin: 20px 0;
                padding-left: 0;
                list-style: none;
            }}
            .benefit-item {{
                margin: 10px 0;
                padding-left: 25px;
                position: relative;
            }}
            .benefit-item::before {{
                content: "✓";
                color: {PRIMARY_COLOR};
                position: absolute;
                left: 0;
                font-weight: bold;
            }}
            .button {{
                background-color: {BUTTON_COLOR};
                color: {BUTTON_TEXT_COLOR};
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 5px;
                display: inline-block;
                font-weight: bold;
                margin: 20px 0;
            }}
            .button:hover {{
                background-color: #008B8B;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 14px;
                color: #707070;
                border-top: 1px solid #E5E5E5;
                padding-top: 20px;
            }}
            .support {{
                color: {PRIMARY_COLOR};
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">
                <img src="https://creativeartsconnect.com/wp-content/uploads/2024/12/Untitled-design.png" alt="Creative Arts Connect Logo">
            </div>
            <div class="content">
                <p>Dear {therapist_name},</p>

                <p>We invite you to join <strong>Creative Arts Connect</strong>, an exclusive online directory designed to connect Art, Music, Drama, Play, Dance and Movement, and Expressive Arts Therapists with individuals and organizations seeking your expertise.</p>

                <h3 style="color: {PRIMARY_COLOR}; margin-top: 24px;">Why Join?</h3>
                <ul class="benefits">
                    <li class="benefit-item">Boost Your Visibility – Showcase your skills to a wider audience.</li>
                    <li class="benefit-item">Build Credibility – Gain trust by being listed in a reputable directory.</li>
                    <li class="benefit-item">Increase Referrals – Attract more clients and new opportunities.</li>
                    <li class="benefit-item">Personalized Profile – Highlight your unique approach, qualifications, and specialties.</li>
                </ul>

                <p><strong>Join today and enjoy your first six months free!</strong></p>

                <a href="{invite_link}" class="button">Join Now</a>

                <p>We’d love to have you on board! If you have any questions, feel free to reach out to us at 
                <a href="mailto:support@creativeartsconnect.com" class="support">support@creativeartsconnect.com</a>.</p>

                <div class="footer">
                    <p>Best regards,<br>
                    The Creative Arts Connect Team<br>
                    <a href="https://www.creativeartsconnect.com" class="support">www.creativeartsconnect.com</a></p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    send_email(email, subject, html_content)


def send_appointment_notification(
    client_email: str,
    therapist_email: str,
    appointment_date: str,
    appointment_time: str,
    description: str = None,
):
    # Send to client
    client_subject = "Your Inquiry Has Been Sent - Creative Arts Connect"
    client_html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: {FONT_FAMILY};
                background-color: {BG_COLOR};
                text-align: left;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                background: #FFFFFF;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .footer {{
                font-size: 12px;
                color: #707070;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <p>Dear Client,</p>

            <p>Thank you for your interest in Creative Arts Connect. We’ve sent your inquiry to the therapist with the following details:</p>

            <ul>
                <li><strong>Date:</strong> {appointment_date}</li>
                <li><strong>Time:</strong> {appointment_time}</li>
                {f'<li><strong>Your Message:</strong> {description}</li>' if description else ''}
            </ul>

            <p>The therapist will get back to you soon to discuss availability and next steps.</p>

            <p>We’re wishing you the best on your therapy journey.</p>

            <p>Warm regards,<br/>
            Creative Arts Connect Team</p>

            <div class="footer">This message was generated by Creative Arts Connect booking system.</div>
        </div>
    </body>
    </html>
    """

    send_email(client_email, client_subject, client_html_content)

    # Send to therapist
    therapist_subject = "Inquiry About a Creative Arts Connect Session"
    therapist_html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: {FONT_FAMILY};
                background-color: {BG_COLOR};
                text-align: left;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                background: #FFFFFF;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .footer {{
                font-size: 12px;
                color: #707070;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <p>Dear Therapist,</p>

            <p>I hope you’re doing well. I came across your profile on Creative Arts Connect and am interested in booking a consultation with you. I would love to learn more about your approach and how Creative Arts Connect can support me.</p>

            <p><strong>A bit about my needs:</strong><br>
            {description or "Not specified by the client."}</p>

            <p>Would you be available for a brief consultation to discuss this further?<br>
            Please let me know your availability and any next steps for booking.</p>

            <p>Looking forward to hearing from you!</p>
            <p>Please Email {client_email} for appointment confirmation.</p>

            <p>Best regards,<br/>
            A prospective client</p>

            <div class="footer">This message was generated by Creative Arts Connect booking system.</div>
        </div>
    </body>
    </html>
    """
    send_email(therapist_email, therapist_subject, therapist_html_content)


def merge_filters(frontend_filters: dict, user_answers: dict):
    merged = {}
    for key, fe_value in frontend_filters.items():
        merged[key] = fe_value or user_answers.get(key)
    return merged


# def get_user_answers_by_user_id(db: Session, user_id: int):
#     from app.models import UserAnswer
#
#     user_answers = (
#         db.query(UserAnswer)
#         .filter(UserAnswer.user_id == user_id)
#         .options(
#             selectinload(UserAnswer.question), selectinload(UserAnswer.selected_options)
#         )
#         .all()
#     )
#
#     answers = {
#         answer.question.text: [
#             opt.option_text for opt in answer.selected_options if opt.option_text
#         ]
#         for answer in user_answers
#     }
#
#     return {
#         # Filters for core search
#         "therapy_types": answers.get(
#             "What type of therapy are you looking for? (Choose all that apply)"
#         ),
#         "client_focus": answers.get("I am looking for therapist who work's with?"),
#         "appointment_type": answers.get("I am looking for…"),
#         "issues": answers.get("Therapists who address (Choose all that apply)"),
#         "languages": answers.get("Which languages do you speak?"),
#         "specializations": answers.get(
#             "I prefer a therapist experienced in (Choose all that apply)"
#         ),
#         # Optional filters you may decide to use
#         "location": answers.get("Select where you live"),
#         "gender_identity": answers.get("How do you identify?"),
#         "age_range": answers.get("How old are you?"),
#         "relationship_status": answers.get("What is your relationship status?"),
#         "religion": answers.get("Which religion do you identify with?"),
#         "therapist_preferences": answers.get(
#             "Any specific preferences for your therapist? (Choose all that apply)"
#         ),
#     }
#
#
# def years_till_now(start_year: int) -> int:
#     now = datetime.now()
#     current_year = now.year
#     current_month = now.month
#
#     years_passed = current_year - start_year
#
#     return years_passed
