let activeConversation = null;

const messages = document.getElementById("messages");
const conversations = document.getElementById("conversations");
const promptBox = document.getElementById("prompt");
const modelSelect = document.getElementById("model");
const errorBox = document.getElementById("error");
const sendButton = document.getElementById("send");

async function api(path, options = {}) {
  const response = await fetch(path, {
    cache: "no-store",
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || `HTTP ${response.status}`);
  return payload;
}

function renderMessages(items) {
  messages.replaceChildren();
  if (!items.length) {
    const empty = document.createElement("div");
    empty.className = "empty";
    empty.textContent = "Start a private conversation with the local model.";
    messages.append(empty);
    return;
  }
  for (const item of items) {
    const article = document.createElement("article");
    article.className = `message ${item.role}`;
    const role = document.createElement("strong");
    role.textContent = item.role === "user" ? "You" : "Local AI";
    const content = document.createElement("div");
    content.textContent = item.content;
    article.append(role, content);
    messages.append(article);
  }
  messages.scrollTop = messages.scrollHeight;
}

async function loadConversations() {
  const payload = await api("/api/conversations");
  conversations.replaceChildren();
  for (const item of payload.conversations) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = item.id === activeConversation ? "conversation active" : "conversation";
    button.textContent = item.title;
    button.addEventListener("click", () => openConversation(item.id));
    conversations.append(button);
  }
}

async function openConversation(id) {
  const conversation = await api(`/api/conversations/${id}`);
  activeConversation = id;
  modelSelect.value = conversation.model;
  renderMessages(conversation.messages);
  await loadConversations();
}

async function initialize() {
  try {
    const [health, modelsPayload] = await Promise.all([
      api("/api/health"),
      api("/api/models"),
    ]);
    const status = document.getElementById("status");
    status.textContent = health.detail;
    status.className = `status ${health.status}`;
    for (const model of modelsPayload.models) {
      const option = document.createElement("option");
      option.value = model;
      option.textContent = model;
      option.selected = model === health.model;
      modelSelect.append(option);
    }
    await loadConversations();
  } catch (error) {
    document.getElementById("status").textContent = error.message;
    errorBox.textContent = error.message;
  }
}

document.getElementById("new-chat").addEventListener("click", async () => {
  activeConversation = null;
  renderMessages([]);
  await loadConversations();
  promptBox.focus();
});

document.getElementById("chat-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = promptBox.value.trim();
  if (!message) return;
  errorBox.textContent = "";
  sendButton.disabled = true;
  promptBox.disabled = true;
  const current = activeConversation
    ? (await api(`/api/conversations/${activeConversation}`)).messages
    : [];
  renderMessages([...current, { role: "user", content: message }, { role: "assistant", content: "Thinking..." }]);
  try {
    const result = await api("/api/chat", {
      method: "POST",
      body: JSON.stringify({
        message,
        conversation_id: activeConversation,
        model: modelSelect.value,
      }),
    });
    activeConversation = result.conversation_id;
    promptBox.value = "";
    await openConversation(activeConversation);
  } catch (error) {
    errorBox.textContent = error.message;
    if (activeConversation) await openConversation(activeConversation);
  } finally {
    sendButton.disabled = false;
    promptBox.disabled = false;
    promptBox.focus();
  }
});

initialize();
