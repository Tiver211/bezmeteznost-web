const modalOverlay = document.getElementById('modalOverlay');
const modalContent = document.querySelector('.modal-content');
const openModalBtn = document.getElementById('openModalBtn');

function showModal() {
  modalOverlay.style.display = 'flex';
  document.body.style.overflow = 'hidden'; // Блокируем прокрутку страницы
}

function hideModal() {
  modalOverlay.style.display = 'none';
  document.body.style.overflow = ''; // Восстанавливаем прокрутку
}

openModalBtn.addEventListener('click', async function() {
  try {
    // Показываем модальное окно сразу с индикатором загрузки
    modalContent.innerHTML = '<div style="text-align: center; padding: 20px;">Загрузка правил...</div>';
    showModal();

    // Загружаем содержимое
    const response = await fetch('static/rules.html');

    if (!response.ok) {
      throw new Error(`Ошибка HTTP! Статус: ${response.status}`);
    }

    const html = await response.text();
    modalContent.innerHTML = html;

    // Добавляем обработчик для кнопки закрытия
    const closeBtn = modalContent.querySelector('.close-modal');
    if (closeBtn) {
      closeBtn.addEventListener('click', hideModal);
    }

  } catch (error) {
    console.error('Ошибка загрузки:', error);
    modalContent.innerHTML = `
      <div style="color: #ff5555; text-align: center; padding: 20px;">
        <p>Не удалось загрузить правила</p>
        <button class="close-modal">Закрыть</button>
      </div>
    `;
    showModal();
  }
});

// Закрытие по клику вне контента
modalOverlay.addEventListener('click', function(e) {
  if (e.target === modalOverlay) {
    hideModal();
  }
});

// Закрытие по ESC
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape' && modalOverlay.style.display === 'flex') {
    hideModal();
  }
});