const history = [];
const chatLog = document.getElementById("chat-log");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");

function renderChatLog() {
  chatLog.innerHTML = "";
  history.forEach(({ role, label, text }) => {
    const div = document.createElement("div");
    div.className = `msg ${role}`;
    if (label) {
      const labelEl = document.createElement("span");
      labelEl.className = "label";
      labelEl.textContent = label;
      div.appendChild(labelEl);
    }
    div.appendChild(document.createTextNode(text));
    chatLog.appendChild(div);
  });
  chatLog.scrollTop = chatLog.scrollHeight;
}

function addMessage(role, text, label) {
  history.push({ role, text, label });
  renderChatLog();
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = chatInput.value.trim();
  if (!message) return;

  addMessage("user", message);
  chatInput.value = "";
  addMessage("system", "The candles flicker...");

  try {
    const res = await fetch("/api/seance", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();

    history.pop(); // remove "flicker..." placeholder

    if (data.error && data.refused) {
      lockTable(data.error);
      return;
    }
    if (data.error) {
      addMessage("system", `⚠️ ${data.error}`);
      return;
    }

    addMessage("board", data.board, "The Ouija Board");
    addMessage("spirit", data.spirit, "The Spirit");

    if (data.refused) {
      lockTable("The spirit refuses to speak with you any longer.");
    }
  } catch (err) {
    history.pop();
    addMessage("system", "⚠️ Network error, try again.");
  }
});

function lockTable(message) {
  chatInput.disabled = true;
  chatInput.placeholder = "The spirit has gone silent...";
  const submitBtn = chatForm.querySelector("button");
  submitBtn.disabled = true;

  document.body.classList.add("candles-out");

  const div = document.createElement("div");
  div.className = "msg system refused";
  div.textContent = `🕸️ ${message}`;
  chatLog.appendChild(div);

  const reloadBtn = document.createElement("button");
  reloadBtn.textContent = "Reload to try again";
  reloadBtn.className = "reload-btn";
  reloadBtn.onclick = () => window.location.reload();
  chatLog.appendChild(reloadBtn);

  chatLog.scrollTop = chatLog.scrollHeight;
}

renderChatLog();
