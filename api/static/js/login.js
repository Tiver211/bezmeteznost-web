async function sendLogin() {
    const mail = document.getElementById('mail').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('error-message');
    const loginContainer = document.querySelector('.login-container');
    const token_obj = document.getElementsByName("smart-token");
    if (token_obj.length === 0) {
        return;
    }
    const token = token_obj[0].value;

    // Очищаем предыдущее сообщение об ошибке и убираем класс тряски
    errorElement.style.display = 'none';
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
          window.smartCaptcha.reset();
          errorElement.style.display = 'grid';
          switch (response.status.toString()) {
              case "401":
                  throw new Error('Login failed');
              case "403":
                  errorElement.textContent = 'Пройдите капчу';

                  loginContainer.classList.add('shake');
                  return;
          }

      }
      if (!response.json().mail_status) {
          window.location.href = '/verify_page';
          return;
      }
      window.location.href = '/';

    } catch (error) {
      console.error('Login error:', error);
      errorElement.textContent = 'Неверные логин или пароль';

      // Добавляем класс с анимацией тряски
      loginContainer.classList.add('shake');
    }
}

function onloadFunction() {
  if (!window.smartCaptcha) {
    return;
  }

  window.smartCaptcha.render('captcha-container', {
    sitekey: 'ysc1_LVBjU7yIahGOgFwLJvUlpoQUYEhywwdtrsNwCfku57778ddd',
    invisible: true, // Сделать капчу невидимой
    callback: sendLogin,
  });
}

function handleSubmit(event) {
  event.preventDefault();

  if (!window.smartCaptcha) {
    return;
  }

  window.smartCaptcha.execute();
}

document.getElementById('loginForm').addEventListener("submit", handleSubmit)