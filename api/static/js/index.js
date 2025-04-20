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
}

function goToDifferentPort() {
    window.location.port = "3876";

}