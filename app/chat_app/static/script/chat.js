const socket = io();
const username = document.body.getAttribute("data-username");

socket.on("connect", () => {
    console.log("Connected as", username);
});

socket.on("disconnect", () => {
    console.log("Disconnected from server");
});

socket.on("message", (msg) => {
    const msgBox = document.getElementById("messages");
    // const isOwnMessage = msg.startsWith(username + ": ");
    const isOwnMessage = msg.username === username; // Check if the message is from the current user

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");
    messageDiv.classList.add(isOwnMessage ? "own" : "other");
    messageDiv.textContent = msg;

    const time = msg.time || "Unknown time"; // Fallback for time if not provided
    messageDiv.innerHTML = `<span class="timestamp">[${time}]</span> <strong>${msg.username}:</strong> ${msg.text}`;

    msgBox.appendChild(messageDiv);
    msgBox.scrollTop = msgBox.scrollHeight; // Scroll to the bottom of the message box

    // msgBox.innerHTML += `<div><strong>${msg}</strong></div>`;
});

function sendMessage() {
    const input = document.getElementById("messageInput");
    const messageText = input.value.trim();

    if (messageText === "") return; // Don't send empty messages

    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const msg = {
        username: username,
        text: messageText,
        time: timestamp
    };

    socket.emit("message", msg); // Send the message object to the server

    // const msg = `${username}: ${input.value}`;
    // socket.send(msg);
    
    input.value = ""; // Clear the input field after sending
}