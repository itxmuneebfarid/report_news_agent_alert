from datetime import datetime, timedelta
from langchain.tools import tool
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

@tool
def get_news(day: str) -> str:
    """Fetch top 10 news headlines for the given date (today, yesterday, or YYYY-MM-DD)."""
    try:
      
        if day.lower() == "today":
            start_date = datetime.now().strftime("%Y-%m-%d")
        elif day.lower() == "yesterday":
            start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            
            try:
                datetime.strptime(day, "%Y-%m-%d")
                start_date = day
            except ValueError:
                return f" Invalid date format: {day}. Please use YYYY-MM-DD."

        tavily = TavilySearch(max_results=10)
        query = f"top news from {start_date} to {start_date}"

        results = tavily.run(query)

        if isinstance(results, list):
            news_items = []
            for idx, item in enumerate(results, 1):
                title = item.get("title", "No title")
                link = item.get("url", "No link")
                news_items.append(f"{idx}. {title}\n    {link}")
            return f" Top News for {start_date}:\n\n" + "\n\n".join(news_items)

        return str(results)
    except Exception as e:
        return f" Error fetching news: {str(e)}"
