// Auto close Bootstrap navbar on mobile after clicking a link
document.addEventListener("DOMContentLoaded", function () {
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");
    const navbar = document.querySelector(".navbar-collapse");

    navLinks.forEach(link => {
        link.addEventListener("click", () => {
            if (navbar.classList.contains("show")) {
                new bootstrap.Collapse(navbar).hide();
            }
        });
    });
});
