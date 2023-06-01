const text = "Flight with Ease!"; 
const delay = 100; // Delay between each character (in milliseconds)

const animatedText = document.querySelector(".animated-text");
let index = 0;

function typeText() {
  animatedText.textContent += text[index];
  index++;
  if (index < text.length) {
    setTimeout(typeText, delay);
  }
}

typeText();