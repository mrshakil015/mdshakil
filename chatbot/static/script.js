// const chatbotToggler = document.querySelector(".chatbot-toggler");
// const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.getElementById("send-btn");


let userMessage = null; // Variable to store user's message
const API_KEY = "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"; // Paste your API key here
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
    // Create a chat <li> element with passed message and className
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi; // return chat <li> element
}

const generateResponse = (chatElement) => {
    const API_URL = "/process_chat";  // Update with your Flask endpoint

    const messageElement = chatElement.querySelector("p");

    // Send POST request to Flask backend
    fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_message: userMessage }),
    })
    .then((res) => res.json())
    .then((data) => {
        messageElement.textContent = data.response_message.trim();
    })
    .catch(() => {
        messageElement.classList.add("error");
        messageElement.textContent =
            "Oops! Something went wrong. Please try again.";
    })
    .finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
};


const handleChat = () => {
    userMessage = chatInput.value.trim(); // Get user entered message and remove extra whitespace
    if(!userMessage) return;

    // Clear the input textarea and set its height to default
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Append the user's message to the chatbox
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);
    
    setTimeout(() => {
        // Display "Thinking..." message while waiting for the response
        const incomingChatLi = createChatLi("Thinking...", "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi);
    }, 600);
}

chatInput.addEventListener("input", () => {
    // Adjust the height of the input textarea based on its content
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // If Enter key is pressed without Shift key and the window 
    // width is greater than 800px, handle the chat
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

// // Simulate click on chatbot toggler button on page load
// window.addEventListener("load", () => {
//     setTimeout(() => {
//         chatbotToggler.click(); // Simulate click on chatbot toggler button
//     }, 1000); // Adjust the delay if needed (in milliseconds)
// });


sendChatBtn.addEventListener("click", handleChat);
// closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
// chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));

const micBtn = document.getElementById("mic-btn");
const recognition = new webkitSpeechRecognition();
recognition.continuous = true; // Set continuous recognition

let isListening = false;
let silenceTimeout;

micBtn.addEventListener("click", () => {
    if (!isListening) {
        micBtn.style.color = "red";
        isListening = true;

        recognition.start();
        recognition.onend = () => {
            micBtn.style.color = "";
            isListening = false;
        };

        recognition.onresult = (event) => {
            clearTimeout(silenceTimeout);

            for (let i = event.resultIndex; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    const transcript = event.results[i][0].transcript;
                    const inputTextArea = document.querySelector(".chat-input textarea");
                    inputTextArea.value += transcript;
                }
            }

            // Reset the silence timeout as speech is detected
            silenceTimeout = setTimeout(() => {
                recognition.stop();
                micBtn.style.color = "";
                isListening = false;
                handleChat(); // Trigger sending the message after the pause
            }, 1500); // Adjust this value to your preference (in milliseconds)
        };
    } else {
        clearTimeout(silenceTimeout);
        recognition.stop();
        micBtn.style.color = "";
        isListening = false;
        handleChat(); // Send the message when the recognition stops
    }
});

