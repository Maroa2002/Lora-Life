let chatBox = document.getElementById("chat-box");
let inputField = document.getElementById("user-input");
let send_btn = document.getElementById("send_btn");

const sendMessage = async () => {
  let userMessage = inputField.value.trim();
  if (userMessage === "") return;

  chatBox.innerHTML += `<p><strong>You:</strong> ${userMessage} </p>`;
  inputField.value = "";

  let url = "http://localhost:5000/chatbot/get_response";
  let response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userMessage }),
  });

  let data = await response.json();
  if (data.reply) {
    chatBox.innerHTML += `<p><strong>Bot:</strong> ${data.reply} </p>`;
  } else {
    chatBox.innerHTML += `<p><strong>Bot:</strong> Sorry, something went wrong. </p>`;
  }

  chatBox.scrollTop = chatBox.scrollHeight;
};

send_btn.addEventListener("click", sendMessage);
