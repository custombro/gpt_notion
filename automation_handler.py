import os
import requests

NOTION_DB = os.getenv("NOTION_DB")
NOTION_CLIENT_ID = os.getenv("NOTION_CLIENT_ID")
NOTION_CLIENT_SECRET = os.getenv("NOTION_CLIENT_SECRET")
NOTION_ACCESS_TOKEN = os.getenv("NOTION_ACCESS_TOKEN")  # OAuth 토큰 (자동 저장됨)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ORDERS_FEED_URL = os.getenv("ORDERS_FEED_URL")
KAKAO_ACCESS_TOKEN = os.getenv("KAKAO_ACCESS_TOKEN")

def get_google_sheet_orders():
    try:
        response = requests.get(ORDERS_FEED_URL)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"❌ Google Sheet Error: {e}"

def update_notion(summary_text):
    url = "https://api.notion.com/v1/pages"

    headers = {
        "Authorization": f"Bearer {NOTION_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "parent": {"database_id": NOTION_DB},
        "properties": {
            "Name": {
                "title": [{"text": {"content": "자동 요약"}}]
            },
            "Summary": {
                "rich_text": [{"text": {"content": summary_text}}]
            }
        }
    }

    res = requests.post(url, json=data, headers=headers)
    return f"✅ Notion Update: {res.text}"

def run_automation():
    orders = get_google_sheet_orders()
    if "❌" in orders:
        return orders

    summary = f"📝 자동 요약 결과:\n{orders[:500]}..."

    notion_result = update_notion(summary)
    return notion_result
