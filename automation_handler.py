import os
import requests

def run_automation_engine():
    notion_token = os.getenv("NOTION_TOKEN")
    notion_db = os.getenv("NOTION_DB")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not notion_token or not notion_db or not openai_key:
        return {"error": "Missing environment variables"}

    # ---------------------------
    # ✅ Step 1: Notion DB 가져오기
    # ---------------------------
    notion_headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    query = requests.post(
        f"https://api.notion.com/v1/databases/{notion_db}/query",
        headers=notion_headers
    ).json()

    pages = query.get("results", [])

    summaries = []

    # ---------------------------
    # ✅ Step 2: 각 페이지 요약
    # ---------------------------
    for page in pages:
        page_id = page["id"]

        blocks = requests.get(
            f"https://api.notion.com/v1/blocks/{page_id}/children",
            headers=notion_headers
        ).json()

        text = ""

        for block in blocks.get("results", []):
            if "paragraph" in block and "rich_text" in block["paragraph"]:
                for t in block["paragraph"]["rich_text"]:
                    text += t.get("plain_text", "") + "\n"

        if not text.strip():
            continue

        # GPT 요약
        gpt = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openai_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-5",
                "messages": [
                    {"role": "system", "content": "요약 작성 assistant"},
                    {"role": "user", "content": f"아래 내용을 한 문단으로 요약해줘:\n{text}"}
                ]
            }
        ).json()

        summary = gpt["choices"][0]["message"]["content"]

        summaries.append({"page_id": page_id, "summary": summary})

    # ---------------------------
    # ✅ Step 3: 결과 업데이트
    # ---------------------------
    for item in summaries:
        update = {
            "properties": {
                "Summary": {
                    "rich_text": [{
                        "text": {"content": item["summary"]}
                    }]
                }
            }
        }

        requests.patch(
            f"https://api.notion.com/v1/pages/{item['page_id']}",
            headers=notion_headers,
            json=update
        )

    return {
        "status": "done",
        "updated_pages": len(summaries)
    }
