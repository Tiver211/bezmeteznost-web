function validatePasswords() {
        const password = document.getElementById('password').value;
        const passwordAgain = document.getElementById('password_again').value;
        const errorElement = document.getElementById('error-message');

        if (password !== passwordAgain) {
          errorElement.style.display = 'grid';
          return false;
        } else {
          errorElement.style.display = 'none';
          return true;
        }
    }

function checkPasswordMatch() {
  const password = document.getElementById('password').value;
  const passwordAgain = document.getElementById('password_again').value;
  const errorElement = document.getElementById('error-message');

  if (password.length === 0 && passwordAgain.length === 0) {
    errorElement.style.display = 'none';
    return;
  }

  if (password !== passwordAgain) {
    errorElement.style.display = 'grid';
    errorElement.textContent = 'Пароли не совпадают';
  } else {
    errorElement.style.display = 'none';
    errorElement.textContent = '';
  }
}

// Добавляем проверку при изменении любого из полей пароля
document.getElementById('password').addEventListener('input', checkPasswordMatch);
document.getElementById('password_again').addEventListener('input', checkPasswordMatch);

async function sendRegister() {

    const mail = document.getElementById('mail').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('error-message');
    const loginContainer = document.querySelector('.login-container');
    const token_obj = document.getElementsByName("smart-token");
    if (token_obj.length === 0) {
        return;
    }
    const token = token_obj[0].value;

    // Очищаем предыдущее сообщение об ошибке и убираем класс тряски
    errorElement.textContent = '';
    loginContainer.classList.remove('shake');

    console.log(username);
    console.log(password);

    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({"mail": mail, "login": username, "password": password, "token": token})
      });

      const status = response.status;

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

              case "409":
                  errorElement.textContent = 'Логин или почта уже заняты';

                  loginContainer.classList.add('shake');
                  return;
          }

      }

      if (!response.ok) {
        throw new Error('Login failed');
      }

      window.location.href = '/';

    } catch (error) {
      console.error('Login error:', error);
      errorElement.textContent = 'Ошибка регистрации';

      // Добавляем класс с анимацией тряски
      loginContainer.classList.add('shake');
    }
  }

function onloadFunction() {
  if (!window.smartCaptcha) {
    return;
  }

  window.smartCaptcha.render('captcha-container', {
    sitekey: 'ysc1_NCBk1wcu1M4sSA1wSODTq5xKxBjzAVuaaLVQi4H4d82297a4,
    invisible: true, // Сделать капчу невидимой
    callback: sendRegister,
  });
}

function handleSubmit(event) {
  event.preventDefault();

  if (!window.smartCaptcha) {
    return;
  }

  window.smartCaptcha.execute();
}

document.getElementById('registerForm').addEventListener("submit", handleSubmit);