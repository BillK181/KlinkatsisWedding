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
    chatbox.innerHTML += `
      <div class="message user">
        <strong>${window.userName}:</strong> ${message}
      </div>
    `;
    chatbox.scrollTop = chatbox.scrollHeight; // Scroll to bottom
    input.value = ''; // Clear input field

    // ------------------- Step 3 -------------------
    // Send the message to the Flask server using fetch
    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

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
        // Error handling if fetch fails
        chatbox.innerHTML += `
          <div class="message bot">
            <strong>Weddingbot:</strong> Error: Could not reach server.
          </div>
        `;
        chatbox.scrollTop = chatbox.scrollHeight;
        console.error("Chat error:", err);
    }
}

// ------------------- Step 6 -------------------
// Attach event listeners when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('chat-input');  // Text input
    const sendBtn = document.getElementById('chat-send'); // Send button
    const bubble = document.getElementById('chatbot-bubble');       // Bubble button
    const container = document.getElementById('chatbot-container'); // Chat container
    const closeBtn = document.getElementById('chatbot-close');      // Close button

    // ------------------- Step 6a -------------------
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

    // ------------------- Step 6b -------------------
    // Show chatbot when bubble is clicked
    bubble.addEventListener('click', () => {
        container.style.display = 'flex';  // show chat
        bubble.style.display = 'none';      // hide bubble

        // ------------------- MOBILE TWEAK -------------------
        // Slightly offset container from top-right corner on mobile
        if (window.innerWidth <= 768) {
            container.style.bottom = '20px';   // leave space from bottom
            container.style.right = '10px';    // slightly offset from edge
            container.style.maxHeight = '80vh'; // taller height when chat is open
        }
    });

    // ------------------- Step 6c -------------------
    // Minimize chatbot when close button is clicked
    closeBtn.addEventListener('click', () => {
        container.style.display = 'none';   // hide chat
        bubble.style.display = 'flex';      // show bubble
        container.style.bottom = '';        // reset bottom
        container.style.right = '';         // reset right
        container.style.maxHeight = '';     // reset maxHeight
    });
});
