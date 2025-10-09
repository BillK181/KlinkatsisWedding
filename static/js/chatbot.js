/**
 * ================== Chatbot JS ==================
 * Handles sending user messages, receiving bot replies,
 * and updating the chat window dynamically.
 */

async function sendMessage(event) {
    // ------------------- Step 0 -------------------
    // Prevent default form submission behavior if this
    // function is triggered by a form submit or Enter key.
    if (event) event.preventDefault();

    // ------------------- Step 1 -------------------
    // Get the input field and chatbox container
    const input = document.getElementById('chat-input');          // User text input
    const chatbox = document.getElementById('chatbot-messages');  // Container for messages

    // Trim whitespace from user's message
    const message = input.value.trim();
    if (!message) return; // If input is empty, do nothing

    // ------------------- Step 2 -------------------
    // Add the user's message to the chatbox
    // We wrap the message in a div with class "message user"
    // and include the user's name (from window.userName)
    chatbox.innerHTML += `
      <div class="message user">
        <strong>${window.userName}:</strong> ${message}
      </div>
    `;
    // Scroll chatbox to the bottom so the latest message is visible
    chatbox.scrollTop = chatbox.scrollHeight;

    // Clear the input field for the next message
    input.value = '';

    // ------------------- Step 3 -------------------
    // Send the message to the Flask server using fetch
    try {
        const res = await fetch("/chat", {
            method: "POST", // Sending POST request
            headers: { "Content-Type": "application/json" }, // Tell server we are sending JSON
            body: JSON.stringify({ message }) // Convert JS object to JSON string
        });

        // Parse JSON response from server
        const data = await res.json();

        // ------------------- Step 4 -------------------
        // Add bot's reply to the chatbox
        chatbox.innerHTML += `
          <div class="message bot">
            <strong>Weddingbot:</strong> ${data.response}
          </div>
        `;
        chatbox.scrollTop = chatbox.scrollHeight; // Scroll down again
    } catch (err) {
        // ------------------- Step 5 -------------------
        // Error handling if fetch fails (e.g., server down)
        chatbox.innerHTML += `
          <div class="message bot">
            <strong>Weddingbot:</strong> Error: Could not reach server.
          </div>
        `;
        chatbox.scrollTop = chatbox.scrollHeight;
        console.error("Chat error:", err); // Log error in console for debugging
    }
}

// ------------------- Step 6 -------------------
// Attach event listeners when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('chat-input'); // Text input
    const sendBtn = document.getElementById('chat-send'); // Send button (add id="chat-send" in HTML)

    // Pressing Enter in the input field triggers sendMessage
    if (input) {
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') sendMessage(e);
        });
    }

    // Clicking the send button triggers sendMessage
    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }
});
document.addEventListener('DOMContentLoaded', function() {
  const bubble = document.getElementById('chatbot-bubble');
  const container = document.getElementById('chatbot-container');
  const closeBtn = document.getElementById('chatbot-close');

  // Show chatbot when bubble is clicked
  bubble.addEventListener('click', () => {
    container.style.display = 'flex';
    bubble.style.display = 'none';
  });

  // Minimize chatbot when close button is clicked
  closeBtn.addEventListener('click', () => {
    container.style.display = 'none';
    bubble.style.display = 'flex';
  });
});
