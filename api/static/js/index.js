const socket = io();

// Элементы DOM
const statusElement = document.getElementById('server-status');
const playersElement = document.getElementById('players-online');

// Обработчик обновления статуса
socket.on('status_update', (data) => {
    console.log('Status update:', data);
    
    // Обновляем статус сервера
    if (data.online) {
        statusElement.innerHTML = '<span class="status-on">Включен</span>';
    } else {
        statusElement.innerHTML = '<span class="status-off">Выключен</span>';
    }
    
    // Обновляем количество игроков
    playersElement.textContent = data.players;
    
    // Обновляем время последней проверки (если нужно)
    if (data.last_check) {
        console.log('Last check:', new Date(data.last_check).toLocaleString());
    }
});

// Обработчики подключения/отключения
socket.on('connect', () => console.log('Connected to WS server'));
socket.on('disconnect', () => console.log('Disconnected from WS server'));

function goToDifferentPort() {
    window.location.href = "http://bezmetejnost.online:3876";
}

async function logout() {
     const response = await fetch ('/api/auth/logout', {
        method: 'POST',
     });
     location.reload();
}
