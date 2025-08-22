from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

@tool
def create_reporting(news_text: str) -> str:
    """Generate a professional daily news report from raw headlines text."""
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

        prompt = f"""
You are a professional journalist assistant preparing a daily report. 
Use ONLY the given headlines.
- Summarize them into a structured report.
- Organize by date.
- Include source links.
- Keep it factual & concise.

Headlines:
{news_text}
"""

        response = llm.invoke(prompt)
        if hasattr(response, "content"):
            if isinstance(response.content, str):
                return response.content
            elif isinstance(response.content, list) and len(response.content) > 0:
           
                chunk = response.content[0]
                if isinstance(chunk, dict) and "text" in chunk:
                    return chunk["text"]
        return str(response)
    except Exception as e:
        return f" Error generating report: {str(e)}"
