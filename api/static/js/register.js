function validatePasswords() {
        const password = document.getElementById('password').value;
        const passwordAgain = document.getElementById('password_again').value;
        const errorElement = document.getElementById('passwordError');
        const matchElement = document.getElementById('passwordMatch');

        if (password !== passwordAgain) {
          errorElement.style.display = 'block';
          matchElement.style.display = 'none';
          return false;
        } else {
          errorElement.style.display = 'none';
          matchElement.style.display = password.length > 0 ? 'block' : 'none';
          return true;
        }
    }

function checkPasswordMatch() {
  const password = document.getElementById('password').value;
  const passwordAgain = document.getElementById('password_again').value;
  const errorElement = document.getElementById('passwordError');
  const matchElement = document.getElementById('passwordMatch');

  if (password.length === 0 && passwordAgain.length === 0) {
    errorElement.style.display = 'none';
    matchElement.style.display = 'none';
    return;
  }

  if (password !== passwordAgain) {
    errorElement.style.display = 'block';
    matchElement.style.display = 'none';
  } else {
    errorElement.style.display = 'none';
    matchElement.style.display = 'block';
  }
}

// Добавляем проверку при изменении любого из полей пароля
document.getElementById('password').addEventListener('input', checkPasswordMatch);
document.getElementById('password_again').addEventListener('input', checkPasswordMatch);

document.getElementById('registerForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const mail = document.getElementById('mail').value;
    const username = document.getElementById('username').value;
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

      if (status == 403) {
          console.error('register error');
          errorElement.textContent = 'Пройдите капчу';

          // Добавляем класс с анимацией тряски
          loginContainer.classList.add('shake');
          return;
      }
      else if (status == 409) {
          console.error('register error');
          errorElement.textContent = 'Логин уже занят, если это ваш логин обратитесь к администрации';

          // Добавляем класс с анимацией тряски
          loginContainer.classList.add('shake');
          return;
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
  });
