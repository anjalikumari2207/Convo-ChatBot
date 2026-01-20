if (typeof window.isSending === "undefined") {
  window.isSending = false;
}

const welcome = document.getElementById("welcome");
const chatBox = document.getElementById("chatBox");

function hideWelcome() {
  if (welcome) welcome.style.display = "none";
}

function quickSend(text) {
  document.getElementById("message").value = text;
  sendMessage();
}

async function sendMessage() {
  if (window.isSending) return;
  window.isSending = true;

  hideWelcome();

  const userId = document.getElementById("userId").value;
  const messageInput = document.getElementById("message");
  const sendButton = document.querySelector(".btn-send");
  const message = messageInput.value.trim();

  if (!message) {
    window.isSending = false;
    return;
  }

  messageInput.value = "";
  messageInput.disabled = true;
  sendButton.disabled = true;

  // User message
  const userMsg = document.createElement("div");
  userMsg.className = "message user animate";
  userMsg.innerHTML = `
    <div class="message-bubble user">
      <div class="message-content">${message}</div>
    </div>
  `;
  chatBox.appendChild(userMsg);

  // Typing indicator
  const typing = document.createElement("div");
  typing.className = "typing-indicator";
  typing.innerHTML = `
    <div class="typing-dots">
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
    </div>
  `;
  chatBox.appendChild(typing);

  try {
    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, message })
    });

    const data = await response.json();
    typing.remove();

    const botMsg = document.createElement("div");
    botMsg.className = "message animate";
    botMsg.innerHTML = `
      <div class="message-bubble ai">
        <div class="message-content">${data.reply}</div>
      </div>
    `;
    chatBox.appendChild(botMsg);

  } catch {
    typing.remove();
  }

  messageInput.disabled = false;
  sendButton.disabled = false;
  window.isSending = false;
}
