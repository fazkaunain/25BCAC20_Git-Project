// Countdown calculation
function updateCountdowns() {
    const elements = document.querySelectorAll(".countdown");

    elements.forEach(el => {
        const date = el.getAttribute("data-date");
        const today = new Date();
        const target = new Date(date);

        const diff = target - today;
        const days = Math.ceil(diff / (1000 * 60 * 60 * 24));

        el.innerText = days > 0 ? days : 0;
    });
}

updateCountdowns();