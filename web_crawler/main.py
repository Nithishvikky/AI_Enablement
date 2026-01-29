import os
import traceback
from datetime import datetime

import boto3
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)  # allow browser requests

bedrock_agent = boto3.client(
    "bedrock-agent-runtime",
    region_name="us-east-1"
)

AGENT_ID = os.getenv("AGENT_ID")
AGENT_ALIAS_ID = os.getenv("AGENT_ALIAS_ID")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        body = request.get_json(force=True)
        user_input = body.get("message", "").strip()

        if not user_input:
            return jsonify({"error": "Message is required"}), 400

        if not AGENT_ID or not AGENT_ALIAS_ID:
            return jsonify({
                "error": "AGENT_ID or AGENT_ALIAS_ID missing"
            }), 500

        session_id = body.get("sessionId")

        if not session_id or not isinstance(session_id, str):
            session_id = f"session-{int(datetime.now().timestamp())}"


        response = bedrock_agent.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=session_id,
            inputText=user_input
        )

        output_text = ""
        event_stream = response.get("completion")

        if event_stream:
            for event in event_stream:
                if "chunk" in event:
                    chunk = event["chunk"]
                    if "bytes" in chunk:
                        output_text += chunk["bytes"].decode("utf-8")

        if not output_text:
            output_text = "Agent returned no output."

        return jsonify({
            "response": output_text,
            "sessionId": session_id
        })

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
