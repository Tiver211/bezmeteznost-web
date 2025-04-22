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
    await checkSet();
}

function goToDifferentPort() {
    window.location.port = "3876";

}

document.getElementById('ipAddress').addEventListener('click', async function() {
  const ipText = this.textContent;
  const feedback = document.querySelector('.copy-feedback');

  try {
    await navigator.clipboard.writeText(ipText);

    // Запускаем анимацию
    feedback.classList.add('animate');
    this.style.color = '#4CAF50';

    // Через 1.5 секунды убираем анимацию
    setTimeout(() => {
      feedback.classList.remove('animate');
      this.style.color = '#000000';
    }, 1500);

  } catch (err) {
    feedback.textContent = 'Ошибка!';
    feedback.style.color = '#f44336';
    feedback.classList.add('animate');

    setTimeout(() => {
      feedback.classList.remove('animate');
      feedback.textContent = 'Скопировано!';
      feedback.style.color = '#4CAF50';
    }, 1500);
  }
});

document.getElementById('setIp').addEventListener('click', function() {
    // Меняем цвет на зелёный
    this.style.backgroundColor = '#4CAF50';
    this.style.color = 'white';

    // Делаем кнопку неактивной
    this.disabled = true;

    // Меняем курсор на "недоступно"
    this.style.cursor = 'not-allowed';

    // Можно добавить текст "Готово"
    this.textContent = 'Установлено!';
});

document.addEventListener('DOMContentLoaded', async function() {
    await checkSet();
});

async function checkSet() {
    const username = document.getElementById('username-input').value;
    const user_ip = document.getElementById('user-ip-input').value;
    const response = await fetch ("api/ips/verify", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({"login": username, "user_ip": user_ip})
    });
    console.log(response);
    if (response.status == 200) {
        const button = document.getElementById('setIp');
        button.style.backgroundColor = '#4CAF50';
        button.style.color = 'white';

        // Делаем кнопку неактивной
        button.disabled = true;

        // Меняем курсор на "недоступно"
        button.style.cursor = 'not-allowed';

        // Можно добавить текст "Готово"
        button.textContent = 'Установлено!';
    }

    else {
        const button = document.getElementById('setIp');
        button.style.backgroundColor = '#007BFF';
        button.style.color = 'white';

        // Делаем кнопку неактивной
        button.disabled = false;

        // Меняем курсор на "недоступно"
        button.style.cursor = 'pointer';

        // Можно добавить текст "Готово"
        button.textContent = 'Установить текущий ip';
    }
}

const button = document.getElementById('clearIps');
    button.addEventListener('click', function() {
        button.style.backgroundColor = '#4CAF50FF';

        setTimeout(function() {
            button.style.backgroundColor = '#007BFF';
        }, 700);
});

function checkMobileOverlap() {
    const title = document.querySelector('.top-title');
    const accountName = document.querySelector('.account-name');
    const menu = document.querySelector('.top-menu');

    if (window.innerWidth <= 768) { // только на мобильных
        const titleRect = title.getBoundingClientRect();
        const nameRect = accountName.getBoundingClientRect();

        // Если правый край заголовка заходит на левый край имени
        if (titleRect.right > nameRect.left) {
            accountName.style.display = 'none';
        } else {
            accountName.style.display = 'inline';
        }
    } else {
        accountName.style.display = 'inline'; // на ПК всегда показываем
    }
}

// Проверяем при загрузке и изменении размера
window.addEventListener('load', checkMobileOverlap);
window.addEventListener('resize', checkMobileOverlap);