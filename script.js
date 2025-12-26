function addMessage(text, className) {
    const chatBox = document.getElementById("chatBox");
    const msg = document.createElement("div");
    msg.className = `message ${className}`;
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        addMessage(data.reply, "bot");

    } catch (error) {
        addMessage("❌ Backend not responding", "bot");
        console.error(error);
    }
}
