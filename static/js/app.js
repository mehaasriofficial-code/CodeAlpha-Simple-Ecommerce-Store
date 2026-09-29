document.addEventListener("DOMContentLoaded", () => {
    const messages = document.querySelectorAll(".message");
    messages.forEach((message) => {
        setTimeout(() => {
            message.style.transition = "opacity 0.4s";
            message.style.opacity = "0";
        }, 3500);
    });

    document.querySelectorAll(".quantity-form input").forEach((input) => {
        input.addEventListener("change", () => {
            const min = Number(input.min || 1);
            const max = Number(input.max || 999);
            let value = Number(input.value);
            if (!Number.isFinite(value)) value = min;
            input.value = Math.max(min, Math.min(max, Math.floor(value)));
        });
    });
});
