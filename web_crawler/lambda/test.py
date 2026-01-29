from lambda_function import lambda_handler


if __name__ == "__main__":
    test_event = {
        "messageVersion": "1.0",
        "function": "web_scraper_tool",
        "parameters": [
            {
            "name": "url",
            "type": "string",
            "value": "https://example.com"
            }
        ],
        "sessionId": "87",
        "agent": {
            "name": "",
            "version": "",
            "id": "",
            "alias": ""
        },
        "actionGroup": "action_group_nithish",
        "sessionAttributes": {},
        "promptSessionAttributes": {},
        "inputText": "scrape this url https://example.com"
    }

    result = lambda_handler(test_event, None)
    print("\n=== Lambda Output ===\n")
    print(result)