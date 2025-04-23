// Heart toggle functionality
const heartIcon = document.querySelector(".now-playing-info .heart");
heartIcon.addEventListener("click", () => {
  heartIcon.classList.toggle("liked");
  if (heartIcon.classList.contains("liked")) {
    heartIcon.setAttribute("aria-pressed", "true");
    heartIcon.setAttribute("title", "Unfavorite");
  } else {
    heartIcon.setAttribute("aria-pressed", "false");
    heartIcon.setAttribute("title", "Favorite");
  }
});
heartIcon.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") {
    e.preventDefault();
    heartIcon.click();
  }
});

// Shuffle toggle functionality
const shuffleCheckbox = document.getElementById("shuffle");
shuffleCheckbox.addEventListener("change", () => {
  if (shuffleCheckbox.checked) {
    alert("Shuffle Stations enabled");
  } else {
    alert("Shuffle Stations disabled");
  }
});

// Explicit filter toggle functionality
const explicitCheckbox = document.getElementById("explicit");
explicitCheckbox.addEventListener("change", () => {
  if (explicitCheckbox.checked) {
    alert("Explicit Filter enabled");
  } else {
    alert("Explicit Filter disabled");
  }
});

// Circular meter functionality (adjust variety)
const circularMeter = document.querySelector(".circular-meter");
const meterProgress = circularMeter.querySelector(".meter-progress");
const percentText = circularMeter.querySelector(".percent");
let varietyPercent = 50; // initial value

function updateMeter(percent) {
  if (percent < 0) percent = 0;
  if (percent > 100) percent = 100;
  varietyPercent = percent;
  const circumference = 2 * Math.PI * 44; // r=44
  const offset = circumference - (circumference * percent) / 100;
  meterProgress.style.strokeDashoffset = offset.toFixed(2);
  percentText.textContent = `${percent}%`;
  circularMeter.setAttribute("aria-valuenow", percent);
  circularMeter.setAttribute("aria-valuetext", `Variety ${percent} percent`);
}

// Click to increase by 10%, loop back to 0 after 100
circularMeter.addEventListener("click", () => {
  let newPercent = varietyPercent + 10;
  if (newPercent > 100) newPercent = 0;
  updateMeter(newPercent);
});

// Keyboard support: left/right arrows to decrease/increase by 5%
circularMeter.addEventListener("keydown", (e) => {
  if (e.key === "ArrowRight" || e.key === "ArrowUp") {
    e.preventDefault();
    let newPercent = varietyPercent + 5;
    if (newPercent > 100) newPercent = 100;
    updateMeter(newPercent);
  } else if (e.key === "ArrowLeft" || e.key === "ArrowDown") {
    e.preventDefault();
    let newPercent = varietyPercent - 5;
    if (newPercent < 0) newPercent = 0;
    updateMeter(newPercent);
  }
});

// Initialize meter on page load
updateMeter(varietyPercent);
