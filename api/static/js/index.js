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

async function logout() {
     const response = await fetch ('/api/auth/logout', {
        method: 'POST',
     });
     location.reload();
}

async function setIp() {
    const response = await fetch('/api/ips/set', {
        method: 'POST',
    });

}

async function clearIps() {
    const response = await fetch('/api/ips/clear', {
        method: 'POST',
    });
}