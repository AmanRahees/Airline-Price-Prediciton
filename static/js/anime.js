const price = 10999
const newText = "₹"+ price

const delay = 200; // Delay between each character (in milliseconds)

const pred = document.querySelector(".pred-body");
let index = 0;

function typeText() {
  pred.textContent += newText[index];
  index++;
  if (index < newText.length) {
    setTimeout(typeText, delay);
  }
}

typeText();