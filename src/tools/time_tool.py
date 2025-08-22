import time
import threading
from src.tools.get_news_tool import get_news
from src.tools.create_report_tool import create_reporting
from src.tools.sending_emails import generate_and_send_report
from src.tools.saving_email_tool import load_emails_from_csv

running_jobs = {}

def _job(day: str):
    """Fetch news, create report, and send to ALL saved emails"""
    news_result = get_news.invoke({"day": day}) if hasattr(get_news, "invoke") else get_news(day)

    if isinstance(news_result, dict) and "news" in news_result:
        news_text = news_result["news"]
    else:
        news_text = str(news_result)

    report = create_reporting.invoke({"news_text": news_text}) \
             if hasattr(create_reporting, "invoke") else create_reporting(news_text)

    for email in load_emails_from_csv():
        print(f" Sending report to {email}")
        if hasattr(generate_and_send_report, "invoke"):
            generate_and_send_report.invoke({"day": day, "user_email": email})
        else:
            generate_and_send_report(day, email)

def schedule_news_report(day: str):
    """Send immediate report to all emails and schedule hourly"""
    _job(day)  
    if "report_scheduler" in running_jobs:
        return "Scheduler already running."

    def loop():
        while True:
            print(" Sending hourly report to all emails...")
            _job(day)
            time.sleep(3600)

    t = threading.Thread(target=loop, daemon=True, name="report_scheduler")
    t.start()
    running_jobs["report_scheduler"] = t
    return "Started hourly scheduler."
