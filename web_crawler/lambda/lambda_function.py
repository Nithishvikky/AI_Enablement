import urllib.request
import urllib.error
import gzip
import io
import json
from html.parser import HTMLParser


MAX_DOWNLOAD_BYTES = 500_000 
MAX_OUTPUT_CHARS = 4000
REQUEST_TIMEOUT = 10


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []

    def handle_data(self, data):
        clean = data.strip()
        if clean:
            self.text_parts.append(clean)

    def get_text(self):
        return " ".join(self.text_parts)


def fetch_url(url: str) -> str:
    print(f"[DEBUG] Fetching URL: {url}")

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; WebCrawler/1.0)",
            "Accept-Encoding": "gzip"
        }
    )

    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        print(f"[DEBUG] HTTP Status: {response.status}")
        raw_data = response.read(MAX_DOWNLOAD_BYTES)
        print(f"[DEBUG] Downloaded bytes: {len(raw_data)}")

        if response.headers.get("Content-Encoding") == "gzip":
            print("[DEBUG] Gzip detected, decompressing")
            raw_data = gzip.GzipFile(fileobj=io.BytesIO(raw_data)).read()

        return raw_data.decode("utf-8", errors="ignore")


def extract_parameters(event):
    params = {}
    for p in event.get("parameters", []):
        if "name" in p and "value" in p:
            params[p["name"]] = p["value"]
    return params


def lambda_handler(event, context):
    print("[DEBUG] Lambda invoked")
    print(f"[DEBUG] Incoming event: {event}")

    
    message_version = event.get("messageVersion", "1.0")
    action_group = event.get("actionGroup", "")
    function_name = event.get("function", "")

    
    params = extract_parameters(event)
    url = params.get("url")

    print(f"[DEBUG] Parsed URL: {url}")

    if not url:
        body_content = {
            "error": "Missing required parameter: url"
        }
    else:
        try:
            html = fetch_url(url)

            parser = TextExtractor()
            parser.feed(html)
            text = parser.get_text()

            if not text:
                text = "No readable text found on the page."

            body_content = {
                "url": url,
                "content": text[:MAX_OUTPUT_CHARS],
                "length": len(text)
            }

            print(f"[DEBUG] Extracted text length: {len(text)}")

        except Exception as e:
            print(f"[ERROR] Exception: {str(e)}")
            body_content = {
                "error": str(e)
            }

    return {
        "messageVersion": message_version,
        "response": {
            "actionGroup": action_group,
            "function": function_name,
            "functionResponse": {
                "responseBody": {
                    "TEXT": {
                        "body": json.dumps(body_content)
                    }
                }
            }
        }
    }
