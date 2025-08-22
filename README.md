# 📰 Report News Agent Alert

An **AI-powered news reporting agent** that automatically fetches, summarizes, and delivers daily news updates.  
The project leverages **Python, FastAPI, and LangChain** along with integration to external APIs and email alerts to keep users informed in real time.

---

##  Introduction

The **Report News Agent Alert** is designed to automate the process of gathering and sharing news.  
Instead of manually browsing multiple websites, this agent:

1. Fetches the latest news articles from reliable sources.  
2. Processes and summarizes the news using **LangChain + LLMs**.  
3. Generates a professional **daily report**.  
4. Sends the report directly to the user’s email inbox.  

This makes it useful for:
- Busy professionals who want quick news digests.  
- Researchers monitoring specific topics.  
- Organizations automating newsletter workflows.  

---
# Project Structure 
```
report_news_agent_alert/
│
├── src/
│ ├── tools/ # Tools for news fetching, email saving, report creation
│ ├── main.py # Entry point for FastAPI server
│ ├── agent.py # News agent logic
│ └── utils/ # Utility functions
│
├── .env # Environment variables (ignored in git)
├── .gitignore # Ignored files (secrets, cache, logs, etc.)
├── README.md # Project documentation
└── requirements.txt # Dependencies
```

##  How It Works

1. **News Retrieval**  
   - The system fetches daily news updates from online sources.  
   - Users can choose specific categories (e.g., technology, politics, health).  

2. **Processing & Summarization**  
   - Raw news is processed using **LangChain** and **Google Generative AI (Gemini)**.  
   - The content is summarized into a concise and readable format.  

3. **Report Generation**  
   - A structured **report file (CSV, PDF, or email body)** is generated.  
   - The report includes headlines, summaries, and source links.  

4. **Email Delivery**  
   - Using Gmail API, the report is sent automatically to the user’s email.  

```

## 🛠️ Tech Stack

- **Backend**: Python (FastAPI)  
- **AI & Processing**: LangChain + Google Generative AI (Gemini)  
- **Database**: CSV/FAISS (for logging and retrieval)  
- **Email Delivery**: Gmail API  
- **Frontend**: HTML + TailwindCSS (for report request UI)  
- **Version Control**: Git & GitHub  

```
