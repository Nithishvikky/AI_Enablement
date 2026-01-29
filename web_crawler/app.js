const API_URL = "http://localhost:8000/chat";

let sessionId = null;

const chatWindow = document.getElementById("chatWindow");
const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

function addMessage(text, cls) {
  const div = document.createElement("div");
  div.className = `message ${cls}`;
  div.textContent = text;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}


async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: text,
        sessionId: sessionId
      })
    });

    const data = await res.json();

    if (!res.ok) {
      addMessage(`Error: ${data.error}`, "bot");
      return;
    }

    sessionId = data.sessionId;
    addMessage(data.response, "bot");

  } catch (err) {
    addMessage("Server not reachable", "bot");
  }
}

sendBtn.onclick = sendMessage;
input.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});


