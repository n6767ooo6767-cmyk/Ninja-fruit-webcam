const list = document.getElementById('game-list');
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('game-container');

// Массив игр (сюда дописывать остальные 49)
const games = {
    snake: {
        name: "Змейка",
        run: () => {
            ctx.fillStyle = "green";
            ctx.fillRect(50, 50, 50, 50); // Тут логика змейки
        }
    },
    pingpong: {
        name: "Пинг-Понг",
        run: () => {
            ctx.fillStyle = "white";
            ctx.fillRect(10, 200, 20, 100); // Логика ракетки
        }
    }
};

// Генерация кнопок
Object.keys(games).forEach(key => {
    let btn = document.createElement('button');
    btn.className = 'neon-btn';
    btn.innerText = games[key].name;
    btn.onclick = () => startGame(key);
    list.appendChild(btn);
});

function startGame(id) {
    document.getElementById('menu').style.display = 'none';
    container.style.display = 'block';
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    function loop() {
        ctx.fillStyle = 'rgba(0,0,0,0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        games[id].run(); // Запуск логики выбранной игры
        requestAnimationFrame(loop);
    }
    loop();
}
