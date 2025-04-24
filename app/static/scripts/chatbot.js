const chatBox = document.getElementById("chat-box");
const inputField = document.getElementById("user-input");
const sendBtn = document.getElementById("send_btn");

const sendMessage = async () => {
  const userMessage = inputField.value.trim();
  if (!userMessage) return;

  chatBox.innerHTML += `<p><strong>You:</strong> ${userMessage} </p>`;
  inputField.value = "";

  // let url = "http://localhost:5000/chatbot/get_response";
  let url = "/chatbot/get_response"; // Use relative URL for production
  let response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userMessage }),
  });

  let data = await response.json();
  if (data.reply) {
    chatBox.innerHTML += `<p><strong>Bot: ${data.language.toUpperCase()} </strong> ${data.reply} </p>`;
  } else {
    chatBox.innerHTML += `<p><strong>Bot:</strong> Sorry, something went wrong. </p>`;
  }

  chatBox.scrollTop = chatBox.scrollHeight;
};

// Send message on button click
sendBtn.addEventListener("click", sendMessage);

// Send message on Enter key press
inputField.addEventListener("keypress", (event) => {
  if (event.key === "Enter") {
    sendMessage();
  }
});