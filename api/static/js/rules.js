const modalOverlay = document.getElementById('modalOverlay');
const modalContent = document.querySelector('.modal-content');
const openModalBtn = document.getElementById('openModalBtn');

openModalBtn.addEventListener('click', async function() {
  // Загружаем содержимое из внешнего файла
  await fetch('static/rules.html')
    .then(response => response.text())
    .then(html => {
      // Вставляем загруженный HTML в модальное окно
      modalContent.innerHTML = html;
      // Показываем модальное окно
      modalOverlay.style.display = 'flex';

      // Добавляем обработчик для кнопки закрытия (если она есть в загружаемом HTML)
      const closeBtn = modalContent.querySelector('.close-modal');
      if(closeBtn) {
        closeBtn.addEventListener('click', () => {
          modalOverlay.style.display = 'none';
        });
      }
    })
    .catch(error => {
      console.error('Ошибка загрузки:', error);
      modalContent.innerHTML = '<p>Не удалось загрузить содержимое</p>';
      modalOverlay.style.display = 'flex';
    });
});