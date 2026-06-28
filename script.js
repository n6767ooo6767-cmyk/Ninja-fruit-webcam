const list = document.getElementById('game-list');
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// --- ЛОГИКА 50 ИГР ---
const games = [
    // Здесь мы создаем массив функций для каждой из 50 игр
    ...Array.from({ length: 50 }, (_, i) => {
        return () => {
            // Уникальная логика для каждой игры на основе ID (i+1)
            ctx.fillStyle = `hsl(${i * 7}, 100%, 50%)`; // Уникальный цвет
            ctx.font = "40px Arial";
            ctx.fillText(`ЭТО ИГРА НОМЕР ${i + 1}`, 50, 100);
            
            // Пример: разные фигуры для разных игр
            if (i % 2 === 0) {
                ctx.fillRect(100, 200, 150, 150); // Квадратная игра
            } else {
                ctx.beginPath();
                ctx.arc(200, 250, 80, 0, Math.PI * 2); // Круглая игра
                ctx.fill();
            }
        };
    })
];

// --- ГЕНЕРАЦИЯ КНОПОК ---
for (let i = 0; i < 50; i++) {
    let btn = document.createElement('button');
    btn.className = 'neon-btn';
    btn.innerText = `Игра ${i + 1}`;
    btn.onclick = () => launchGame(i);
    list.appendChild(btn);
}

// --- ЗАПУСК ---
function launchGame(id) {
    document.getElementById('menu').style.display = 'none';
    document.getElementById('game-container').style.display = 'block';
    
    function loop() {
        ctx.fillStyle = 'rgba(0,0,0,0.2)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Вызываем логику конкретной игры
        games[id](); 
        
        requestAnimationFrame(loop);
    }
    loop();
}

document.addEventListener('DOMContentLoaded', () => {
    const list = document.getElementById('game-list');
    
    // Создаем кнопки
    for (let i = 1; i <= 50; i++) {
        let btn = document.createElement('button');
        btn.className = 'neon-btn';
        btn.innerText = `Игра ${i}`;
        btn.style.cssText = `border-color: hsl(${i * 7}, 100%, 50%); color: hsl(${i * 7}, 100%, 50%);`;
        btn.onclick = () => alert("Запуск игры " + i); // Тестовый клик
        list.appendChild(btn);
    }
});
