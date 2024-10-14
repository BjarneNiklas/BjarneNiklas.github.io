const images = [];
const imgElement = document.getElementById('rotatingDisc');

// All PNG names: SW0_0.png, SW1_15.png, ..., SW23_345.png
for (let i = 0; i < 24; i++) {
  let angle = i * 15; // 0, 15, 30, ..., 345
  images.push(`BjarneNiklas.github.io/images/SW${i}_${angle}.png`);
}

let currentFrame = 0;

function rotateDisc() {
  currentFrame = (currentFrame + 1) % images.length;
  imgElement.src = images[currentFrame];
}

let rotationInterval;

document.addEventListener('keydown', (event) => {
  if (event.key === 'a') {
    if (rotationInterval) {
      clearInterval(rotationInterval); // Stop animation
      rotationInterval = null;
    } else {
      rotationInterval = setInterval(rotateDisc, 100); // Start animation
    }
  } else if (event.key === 'l') {
    currentFrame = (currentFrame - 1 + images.length) % images.length;
    imgElement.src = images[currentFrame];
  } else if (event.key === 'r') {
    currentFrame = (currentFrame + 1) % images.length;
    imgElement.src = images[currentFrame];
  }
});

const spriteElement = document.querySelector('.sprite');
const spriteWidth = 52;
let currentSpriteFrame = 0;
const totalSpriteFrames = 19;
let spriteAnimationInterval;
let isAnimating = false;

function animateSprite() {
  if (currentSpriteFrame < totalSpriteFrames) {
    const newPosition = `-${currentSpriteFrame * spriteWidth}px 0`; 
    spriteElement.style.backgroundPosition = newPosition;
    currentSpriteFrame++;
  } else {
    clearInterval(spriteAnimationInterval);
    isAnimating = false;
  }
}

// Start animation
function startSpriteAnimation() {
  currentSpriteFrame = 0;
  isAnimating = true;
  spriteAnimationInterval = setInterval(animateSprite, 250);
}

// Start animaton automatically by start
startSpriteAnimation();

// Restart Animation
document.addEventListener('keydown', (event) => {
  if (event.key === ' ') { // Leertaste
    if (!isAnimating) {
      startSpriteAnimation();
    }
  }
});
