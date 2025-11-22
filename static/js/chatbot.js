//Chatbot JS

async function sendMessage(event) {
    // Prevent default form submission behavior if this function is triggered by a form submit or Enter key.
    if (event) event.preventDefault();

    // Get the input field and chatbox container
    const input = document.getElementById('chat-input');         
    const chatbox = document.getElementById('chatbot-messages'); 

    // Trim whitespace from user's message
    const message = input.value.trim();
    if (!message) return; 

    // Add the user's message to the chatbox
    chatbox.innerHTML += `
      <div class="message user">
        <strong>${window.userName}:</strong> ${message}
      </div>
    `;
    chatbox.scrollTop = chatbox.scrollHeight; 
    input.value = ''; 

    // Send the message to the Flask server using fetch
    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await res.json();

        // Add bot's reply to the chatbox
        chatbox.innerHTML += `
          <div class="message bot">
            <strong>Wedding Specialist:</strong> ${data.response}
          </div>
        `;
        chatbox.scrollTop = chatbox.scrollHeight; // Scroll down again
    } catch (err) {
        // Error handling if fetch fails
        chatbox.innerHTML += `
          <div class="message bot">
            <strong>Wedding Specialist:</strong> Error: Could not reach server.
          </div>
        `;
        chatbox.scrollTop = chatbox.scrollHeight;
        console.error("Chat error:", err);
    }
}

// Attach event listeners when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('chat-send'); 
    const bubble = document.getElementById('chatbot-bubble');
    const container = document.getElementById('chatbot-container');
    const closeBtn = document.getElementById('chatbot-close');      

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

    // Show chatbot when bubble is clicked
    bubble.addEventListener('click', () => {
        container.style.display = 'flex'; 
        bubble.style.display = 'none';   

        // Slightly offset container from top-right corner on mobile
        if (window.innerWidth <= 768) {
            container.style.bottom = '20px';  
            container.style.right = '10px';    
            container.style.maxHeight = '80vh'; 
        }
    });

    // Minimize chatbot when close button is clicked
    closeBtn.addEventListener('click', () => {
        container.style.display = 'none';  
        bubble.style.display = 'flex';     
        container.style.bottom = '';        
        container.style.right = '';         
        container.style.maxHeight = '';  
    });
});
