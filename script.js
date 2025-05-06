const earthImg = document.getElementById("earthImage");
const video = document.getElementById("earthVideo");
const nepalContainer = document.getElementById("nepalContainer");
const text = document.getElementById("textBlock");

let hasScrolled = false;

// Reusable function to start the video transition
function playZoomVideo() {
  if (hasScrolled) return;
  hasScrolled = true;

  // Earth → Video
  earthImg.classList.remove("visible");
  earthImg.classList.add("hidden");

  text.classList.add("hidden");

  video.classList.remove("hidden");
  video.classList.add("visible");

  video.play();
}

// Scroll to play
window.addEventListener("wheel", (e) => {
  if (e.deltaY > 10) {
    playZoomVideo();
  }
});

// Click to play
window.addEventListener("click", () => {
  playZoomVideo();
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
    }, 2000);
  }, 2000);
});
