const earthImg = document.getElementById("earthImage");
const video = document.getElementById("earthVideo");
const nepalContainer = document.getElementById("nepalContainer");
const text = document.getElementById("textBlock");

let hasScrolled = false;

window.addEventListener("wheel", (e) => {
  if (!hasScrolled && e.deltaY > 10) {
    hasScrolled = true;

    // Earth → Video
    earthImg.classList.remove("visible");
    earthImg.classList.add("hidden");

    text.classList.add("hidden");

    video.classList.remove("hidden");
    video.classList.add("visible");

    video.play();
  }
});

video.addEventListener("ended", () => {
  // Video → Nepal Map
  video.classList.remove("visible");
  video.classList.add("hidden");

  nepalContainer.classList.remove("hidden");
  nepalContainer.classList.add("visible");

  // 2s later → fade to black
  setTimeout(() => {
    nepalContainer.classList.add("fade-to-black");
    setTimeout(() => {
        window.location.href = "portfolio.html";
    }
    , 2000);
  }, 2000);

});
