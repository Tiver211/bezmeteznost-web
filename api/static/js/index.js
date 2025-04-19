const ws = new WebSocket("ws://localhost:8000/ws");

ws.onmessage = function(event) {
    const message = event.data;
    document.getElementById("messages").innerHTML += "<div>" + message + "</div>";
};

function sendMessage() {
    const input = document.getElementById("messageInput");
    ws.send(input.value);
    input.value = '';
}

// Функция для отображения/скрытия меню аккаунта
function toggleMenu() {
    const menu = document.getElementById("accountMenu");
    menu.style.display = menu.style.display === "block" ? "none" : "block";
}
