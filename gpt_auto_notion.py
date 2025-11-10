import os
import requests
from flask import jsonify

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB = os.getenv("NOTION_DB")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def add_task_to_notion(task_title, task_note=""):
    """
    ✅ Notion DB에 새 Task 추가
    """
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    payload = {
        "parent": {"database_id": NOTION_DB},
        "properties": {
            "Name": {"title": [{"text": {"content": task_title}}]},
            "Description": {"rich_text": [{"text": {"content": task_note}}]}
        }
    }

    res = requests.post(url, headers=headers, json=payload)
    return res.status_code, res.json()


def auto_brain(prompt):
    """
    ✅ GPT-5 API 호출 → 결과를 문자열로 리턴
    """
    import openai
    openai.api_key = OPENAI_KEY

    res = openai.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


def automation_handler():
    """
    ✅ 실제 자동화 로직
    (예: 오늘 주문 요약 → Notion Task로 저장)
    """
    summary = auto_brain("오늘 할 일 요약 5줄로 만들어줘.")
    code, result = add_task_to_notion("오늘 작업 요약", summary)
    return {"notion_status": code, "summary": summary}
