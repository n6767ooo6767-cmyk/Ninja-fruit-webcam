const list = document.getElementById('game-list');
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const menu = document.getElementById('menu');
const gameContainer = document.getElementById('game-container');

// 1. Создаем движок, который умеет запускать разные игры
const gameEngine = {
    // Тут мы описываем логику для каждой игры (по номеру)
    run: (id) => {
        // Очищаем экран каждый кадр
        ctx.fillStyle = "black";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Логика зависит от ID игры
        if (id === 1) { // Игра 1: Простой кликер
            ctx.fillStyle = "white";
            ctx.fillText("КЛИКНИ НА ЭКРАН!", 50, 50);
        } else if (id === 2) { // Игра 2: Движущийся квадрат
            ctx.fillStyle = "red";
            let x = (Date.now() / 10) % canvas.width;
            ctx.fillRect(x, 100, 50, 50);
        } else {
            ctx.fillStyle = "gray";
            ctx.fillText("Игра №" + id + " в разработке...", 50, 50);
        }
    }
};

// 2. Генерируем 50 кнопок
for (let i = 1; i <= 50; i++) {
    let btn = document.createElement('button');
    btn.className = 'neon-btn';
    btn.innerText = `Игра ${i}`;
    btn.onclick = () => startTheGame(i);
    list.appendChild(btn);
}

// 3. Функция запуска (переход в режим игры)
function startTheGame(id) {
    menu.style.display = 'none';
    gameContainer.style.display = 'block';
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    function loop() {
        gameEngine.run(id); // Запускаем логику игры по ID
        requestAnimationFrame(loop);
    }
    loop();
}
