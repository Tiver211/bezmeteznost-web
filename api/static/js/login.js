document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const mail = document.getElementById('mail').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('error-message');
    const loginContainer = document.querySelector('.login-container');
    const token_obj = document.getElementsByName("smart-token");
    if (token_obj.lenght == 0) {
        return;
    }
    const token = token_obj[0].value;

    // Очищаем предыдущее сообщение об ошибке и убираем класс тряски
    errorElement.textContent = '';
    loginContainer.classList.remove('shake');

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({"mail": mail, "password": password, "token": token })
      });

      if (!response.ok) {
          switch (response.status.toString()) {
              case "401":
                  throw new Error('Login failed');
              case "403":
                  errorElement.textContent = 'Пройдите капчу';

                  loginContainer.classList.add('shake');
                  return;
          }

      }

      window.location.href = '/';

    } catch (error) {
      console.error('Login error:', error);
      errorElement.textContent = 'Неверные логин или пароль';

      // Добавляем класс с анимацией тряски
      loginContainer.classList.add('shake');
    }
  });