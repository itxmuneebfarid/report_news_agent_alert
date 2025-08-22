
import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.tools.saving_email_tool import save_email_to_csv
from src.tools.create_report_tool import create_reporting
from src.tools.get_news_tool import get_news
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    email: str

class ReportRequest(BaseModel):
    user_email: str
    day: str = "today"

def send_email_gmail(to_email: str, subject: str, html_content: str) -> str:
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
    try:
        save_email_to_csv(user_email)

        news_text = get_news.invoke({"day": day}) if hasattr(get_news, "invoke") else get_news(day)
        if not news_text:
            raise RuntimeError("No news data retrieved.")

        report_text = create_reporting.invoke({"news_text": news_text}) \
                      if hasattr(create_reporting, "invoke") else create_reporting(news_text)
        if not report_text:
            raise RuntimeError("Report creation failed, empty text.")

        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        prompt = f"""
        Convert the following report into clean HTML
        with h2/h3 headlines and simple styling.
        Do not include markdown or <html>/<body> tags.

        Report content:
        {report_text}
        """
        html_report = llm.invoke(prompt).content.strip()
        if html_report.startswith("```"):
            html_report = html_report.strip("`").replace("html", "", 1).strip()

        send_email_gmail(
            to_email=user_email,
            subject=f"Hourly News Report - {day}",
            html_content=html_report
        )
        return f"Report sent successfully to {user_email}!"

    except Exception as e:
        return f"Failed to send report to {user_email}: {str(e)}"


@app.post("/save_email")
def save_email(request: EmailRequest):
    save_email_to_csv(request.email)
    return {"status": "success", "message": f"Email {request.email} saved!"}

@app.post("/generate_report")
def generate_report(request: ReportRequest):
    result = generate_and_send_report(request.day, request.user_email)
    return {"status": "success", "message": result}

@app.get("/")
def root():
    return {"status": "running", "message": "Server is live"}
