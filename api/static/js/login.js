document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('error-message');
    const loginContainer = document.querySelector('.login-container');

    // Очищаем предыдущее сообщение об ошибке и убираем класс тряски
    errorElement.textContent = '';
    loginContainer.classList.remove('shake');

    console.log(username);
    console.log(password);

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      window.location.href = '/';

    } catch (error) {
      console.error('Login error:', error);
      errorElement.textContent = 'Неверные логин или пароль';

      // Добавляем класс с анимацией тряски
      loginContainer.classList.add('shake');
    }
  });