// Lightbox for the gallery page

const links = [...document.querySelectorAll(".photo a")];
const box = document.querySelector(".lightbox");
const image = box.querySelector("img");
const caption = box.querySelector(".caption");
let current = 0;

function show(i) {
  current = (i + links.length) % links.length;
  const link = links[current];
  if (image.src !== link.href) {
    image.style.opacity = 0; // hide the previous photo until the new one loads
    image.src = link.href;
  }
  image.alt = link.dataset.place;
  caption.textContent = link.dataset.place;
  if (link.dataset.date) {
    const date = document.createElement("span");
    date.textContent = ` · ${link.dataset.date}`;
    caption.append(date);
  }
  box.hidden = false;
}

function close() {
  box.hidden = true;
  links[current].focus();
}

image.addEventListener("load", () => { image.style.opacity = 1; });

links.forEach((link, i) => link.addEventListener("click", e => {
  e.preventDefault();
  show(i);
}));

box.querySelector(".close").addEventListener("click", close);
box.querySelector(".prev").addEventListener("click", () => show(current - 1));
box.querySelector(".next").addEventListener("click", () => show(current + 1));
box.addEventListener("click", e => { if (e.target === box) close(); });

document.addEventListener("keydown", e => {
  if (box.hidden) return;
  if (e.key === "Escape") close();
  if (e.key === "ArrowLeft") show(current - 1);
  if (e.key === "ArrowRight") show(current + 1);
});
