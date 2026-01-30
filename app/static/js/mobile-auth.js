document.addEventListener("DOMContentLoaded", () => {
  const screens = document.querySelectorAll(".mobile-screen");

  screens.forEach(screen => {
    const bg = getComputedStyle(screen).getPropertyValue("--bg-image");
    if (!bg) return;

    const url = bg.replace(/url\(["']?(.*?)["']?\)/, "$1");
    const img = new Image();

    img.src = url;
    img.onload = () => {
      screen.classList.add("is-loaded");
    };
  });
});
