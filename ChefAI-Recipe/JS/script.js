let dishPrompt = document.querySelector("#prompt");
let chatContainer = document.querySelector(".chat-container");


function createChatBox(html,classes){
    let div = document.createElement("div");
    div.innerHTML = html;
    div.classList.add(classes);
    return div;
}

function handleChatResponse(message){
    let html = ` <img src="assets/user.png" alt="" id = "userImage" width="50">
            <div class="user-chat-area">${message}</div>`
    
    let userChatBox = createChatBox(html,"user-chat-box");
    chatContainer.appendChild(userChatBox);

    setTimeout(async ()=>{
        let html = ` <img src="assets/ai.png" alt="" id = "aiImage" width="70">
            <div class="ai-chat-area"><img src="assets/bouncing_dots.gif" alt="" class="load" width="50px"></div>`

        let aiChatBox = createChatBox(html,"ai-chat-box");
        chatContainer.appendChild(aiChatBox);
        let response = generateResponse(message);
        console.log(response);

    },600);


}

dishPrompt.addEventListener("keydown" , (e) =>{
    if(e.key == "Enter"){
        handleChatResponse(dishPrompt.value);
        dishPrompt.value = "";
    }
});