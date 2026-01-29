# Web-Crawler Agent using AWS Bedrock

## Overview
This project implements a Web-Crawler Agent using AWS Bedrock that accepts user questions to crawl URLs and return clean text content. The agent is deployed as an AWS Lambda function and exposed through a simple HTML frontend interface with real-time chat functionality.

## Important Files

- `lambda/lambda_function.py` - AWS Lambda function that handles web scraping with gzip, redirects, and size limits (registered as web_scrape _tool in Bedrock)
- `lambda/test.py` - Local testing script for the Lambda function
- `main.py` - Flask backend server that communicates with Bedrock Agent Runtime API and handles chat sessions
- `index.html` - Frontend chat interface for user interaction with the Bedrock agent
- `app.js` - Frontend JavaScript handling user input, API calls to Flask backend, and chat display logic
- `styles.css` - Styling for the chat interface

## Amazon Bedrock Agent Configuration

### Model Used
**Claude 3.7 Sonnet**

### System Instruction
```
You are a web-crawler agent.

Your role is to help users extract readable text from web pages.

When a user asks to crawl, scrape, fetch, or read a URL:
- You MUST call the web_scrape tool
- Pass the URL exactly as provided by the user
- Do not modify, shorten, or invent URLs

The web_scrape tool fetches the page content and handles redirects, gzip compression, and size limits.

After receiving the tool response:
- Return clean, readable plain text snippets
- If the content is long, summarize it clearly
- Do not include HTML, JavaScript, CSS, or raw markup

If the tool returns an error:
- Explain the failure clearly and concisely

Do not claim to browse the web directly.
Always rely on the web_scrape tool for web content.
```

### Action Group & Lambda Integration
- **Action Group Name**: action_group_nithish
- **Lambda Function**: `dummy_lambda.py` deployed as AWS Lambda
- **Tool Name**: `web_scraper_tool`
- **Arguments**: Accepts `url` as string
- **Function**: Handles URL fetching, HTML parsing, text extraction with proper error handling
- **Features**: Supports gzip compression, redirects, size limits (500KB max), timeout handling (10s)

## Frontend Implementation

### Tech Stack
- **Frontend**: Pure HTML5, CSS3, and Vanilla JavaScript
- **Backend**: Python Flask with CORS enabled
- **Communication**: REST API using JSON format

### Backend Connection
- **Endpoint**: `POST http://localhost:8000/chat`
- **Frontend (app.js)** sends user messages to Flask backend
- **Backend (main.py)** forwards requests to Bedrock Agent Runtime API
- **Real-time chat** with session management using dynamically generated session IDs
- **Error handling** for server connectivity and Bedrock API issues
- **Auto-scroll** chat window and Enter key support for message sending

### Setup & Usage
1. Configure `.env` file with your Bedrock AGENT_ID and AGENT_ALIAS_ID
2. Install dependencies: `pip install -r requirements.txt`
3. Run backend: `python main.py`
4. Open `index.html` in browser
5. Ask the agent to crawl URLs: "Crawl this URL: https://example.com"
