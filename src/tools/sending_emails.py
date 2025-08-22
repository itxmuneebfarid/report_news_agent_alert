import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from src.tools.create_report_tool import create_reporting
from src.tools.get_news_tool import get_news
from src.tools.saving_email_tool import save_email_to_csv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def send_email_gmail(to_email: str, subject: str, html_content: str) -> str:
    """Send an email via Gmail API using credentials.json"""
    creds = Credentials.from_authorized_user_file("credentials.json", SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEMultipart()
    message['to'] = to_email
    message['subject'] = subject
    message.attach(MIMEText(html_content, 'html'))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    try:
        sent = service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
        return f"Email sent successfully! Message ID: {sent['id']}"
    except Exception as e:
        raise RuntimeError(f"Gmail API failed: {e}")

def generate_and_send_report(day: str, user_email: str) -> str:
    """Generate daily news report and send it via Gmail API"""
    try:
        print(f"Starting report generation for {user_email} ({day})")
        save_email_to_csv(user_email)
        print("Fetching news...")
        news_text = get_news.invoke({"day": day}) if hasattr(get_news, "invoke") else get_news(day)
        if not news_text:
            raise RuntimeError("No news data retrieved.")
        print(" News fetched.")

        print("Creating report...")
        report_text = create_reporting.invoke({"news_text": news_text}) \
                      if hasattr(create_reporting, "invoke") else create_reporting(news_text)
        if not report_text:
            raise RuntimeError("Report creation failed, got empty text.")
        print(" Report created.")

        print(" Converting to HTML...")
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        prompt = f"""
        Convert the following report into a clean HTML page
        with clear headlines (h2, h3) and simple styling.
        Do not include markdown code fences or <html>/<body> wrappers.

        Report content:
        {report_text}
        """
        html_report = llm.invoke(prompt).content.strip()
        if html_report.startswith("```"):
            html_report = html_report.strip("`").replace("html", "", 1).strip()
        print(" HTML generated.")

       
        print("Sending email via Gmail API...")
        result = send_email_gmail(
            to_email=user_email,
            subject=f"Hourly News Report - {day}",
            html_content=html_report
        )
        print(result)
        return f"Report sent successfully to {user_email}!"

    except Exception as e:
        error_msg = f" Failed to send report to {user_email}: {str(e)}"
        print(error_msg)
        return error_msg
