let dishPrompt = document.querySelector("#prompt");
let chatContainer = document.querySelector(".chat-container");

async function getRecipe(prompt) {
    try {
        let response = await fetch("http://localhost:5000/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt })
        });

        let data = await response.json();
        return data.recipe;   
    } catch (error) {
        console.error("Error:", error);
        return "⚠️ Error connecting to server.";
    }
    
}



function createChatBox(html, classes) {
    let div = document.createElement("div");
    div.innerHTML = html;
    div.classList.add(classes);
    return div;
}

async function handleChatResponse(message) {
    // --- USER MESSAGE ---
    let html = ` 
        <img src="assets/user.png" alt="" id="userImage" width="50">
        <div class="user-chat-area">${message}</div>`;
    
    let userChatBox = createChatBox(html, "user-chat-box");
    chatContainer.appendChild(userChatBox);

    // --- AI LOADING BOX ---
    let aiHtml = `
        <img src="assets/ai.png" alt="" id="aiImage" width="70">
        <div class="ai-chat-area">
            <img src="assets/bouncing_dots.gif" alt="" class="load" width="50px">
        </div>`;
    
    let aiChatBox = createChatBox(aiHtml, "ai-chat-box");
    chatContainer.appendChild(aiChatBox);

    // --- FETCH RECIPE ---
    let response = await getRecipe(message);

    // Replace loading dots with actual response which is converted into markdown
    aiChatBox.querySelector(".ai-chat-area").innerText = response;
    chatContainer.scrollTo({
        top: chatContainer.scrollHeight,
        behavior: "smooth"
    });
}

dishPrompt.addEventListener("keydown", (e) => {
    if (e.key == "Enter" && dishPrompt.value.trim() !== "") {
        handleChatResponse(dishPrompt.value);
        dishPrompt.value = "";
    }
});
