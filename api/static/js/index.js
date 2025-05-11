// Функция для получения статуса сервера
function fetchServerStatus() {
    const statusElement = document.getElementById('server-status');
    const playersElement = document.getElementById('players-online');

    // Запрашиваем данные с API
    fetch('/api/ips/server_status')
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка сети');
            }
            return response.json();
        })
        .then(data => {
            // Обновляем статус сервера
            if (data.status) {
                statusElement.innerHTML = '<span class="status-on">Включен</span>';
            } else {
                statusElement.innerHTML = '<span class="status-off">Выключен</span>';
            }

            // Обновляем количество игроков
            playersElement.textContent = `${data.players}`;
        })
        .catch(error => {
            console.error('Ошибка при получении статуса сервера:', error);
            statusElement.innerHTML = '<span class="status-off">Ошибка загрузки</span>';
            playersElement.textContent = '?';
        });
}

function goToDifferentPort() {
    window.location.port = "3876";
}

async function logout() {
     const response = await fetch ('/api/auth/logout', {
        method: 'POST',
     });
     location.reload();
}

// Загружаем статус при открытии страницы
document.addEventListener('DOMContentLoaded', fetchServerStatus);

// Обновляем статус каждые 30 секунд
setInterval(fetchServerStatus, 30000);
