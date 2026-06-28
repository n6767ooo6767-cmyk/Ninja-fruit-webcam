// =========================
// MiniVerse v1.0
// script.js
// =========================

console.log("MiniVerse loaded!");

// Анимация появления карточек
const cards = document.querySelectorAll(".category, .game-card");

cards.forEach((card, index) => {

    card.style.opacity = "0";
    card.style.transform = "translateY(30px)";

    setTimeout(() => {

        card.style.transition = "0.5s";
        card.style.opacity = "1";
        card.style.transform = "translateY(0px)";

    }, index * 120);

});

// Клик по категориям
document.querySelectorAll(".category").forEach(category => {

    category.addEventListener("click", () => {

        const name = category.querySelector("h3").textContent;

        alert("Раздел \"" + name + "\" скоро появится!");

    });

});

// Кнопки Play
document.querySelectorAll(".game-card button").forEach(button => {

    button.addEventListener("click", () => {

        const game = button.parentElement.querySelector("h3").textContent;

        alert("Запуск игры: " + game);

        // Потом заменим на:
        // location.href = "games/.../index.html";

    });

});

// Параллакс карточек
document.addEventListener("mousemove", e => {

    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;

    cards.forEach(card => {

        card.style.transform =
            `rotateY(${(x - 0.5) * 6}deg)
             rotateX(${(0.5 - y) * 6}deg)`;

    });

});

// Возврат положения
document.addEventListener("mouseleave", () => {

    cards.forEach(card => {

        card.style.transform = "";

    });

});

// Эффект нажатия
cards.forEach(card => {

    card.addEventListener("mousedown", () => {

        card.style.transform += " scale(.96)";

    });

    card.addEventListener("mouseup", () => {

        card.style.transform = "";

    });

});

// Небольшое приветствие
setTimeout(() => {

    console.log("Добро пожаловать в MiniVerse!");

}, 1000);
