document.addEventListener("DOMContentLoaded", function () {

    const btn = document.querySelector(".user-btn");
    const menu = document.querySelector(".dropdown-menu");

    if (!btn || !menu) return;

    btn.addEventListener("click", function (e) {
        e.stopPropagation();
        menu.classList.toggle("show");
    });

    document.addEventListener("click", function () {
        menu.classList.remove("show");
    });

});