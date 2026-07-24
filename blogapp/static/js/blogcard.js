
document.querySelectorAll(".blog-card").forEach(card => {

    card.addEventListener("pointerup", function () {

        this.classList.add("pressed");

        setTimeout(() => {
            window.location.href = this.dataset.href;
        }, 100);

    });

});
