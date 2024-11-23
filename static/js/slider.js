class SlideManager {
  constructor() {
    this.currentSlide = 0;
  }

  nextSlide() {
    this.showSlide(this.currentSlide + 1);
  }

  prevSlide() {
    this.showSlide(this.currentSlide - 1);
  }

  goToSlide(index) {
    this.showSlide(index);
  }

  showSlide(index) {
    const slides = document.querySelectorAll(".slide");
    const paginationButtons = document.querySelectorAll(".pagination-button");

    if (index >= slides.length) {
      if (isLoopEnabled) {
        this.currentSlide = 0;
      } else {
        this.currentSlide = slides.length - 1;
      }
    } else if (index < 0) {
      if (isLoopEnabled) {
        this.currentSlide = slides.length - 1;
      } else {
        this.currentSlide = 0;
      }
    } else {
      this.currentSlide = index;
    }

    slides.forEach((slide, i) => {
      slide.style.display = i === this.currentSlide ? "block" : "none";
    });

    paginationButtons.forEach((button, i) => {
      button.classList.toggle("active", i === this.currentSlide);
    });
  }
}

let autoSlideInterval = null;
let isLoopEnabled = false;
const slideManager = new SlideManager();

document.addEventListener("DOMContentLoaded", () => {
  const settings = document.querySelector("#slider").dataset;
  isLoopEnabled = settings.loop === "True";

  slideManager.showSlide(0);

  if (settings.auto === "True") autoSlide();

  const sliderElement = document.querySelector("#slider");

  sliderElement.addEventListener("mouseenter", () => {
    if (settings.auto === "True" && settings.stopmousehover === "True") {
      clearInterval(autoSlideInterval);
    }
  });

  sliderElement.addEventListener("mouseleave", () => {
    if (settings.auto === "True" && settings.stopmousehover === "True") {
      autoSlide();
    }
  });

  document.querySelectorAll(".slide").forEach((slide) => {
    slide.addEventListener("click", function () {
      const link = slide.parentElement.getAttribute("href");
      if (link) {
        window.location.href = link;
      }
    });
  });
});

function nextSlide() {
  slideManager.nextSlide();
}

function prevSlide() {
  slideManager.prevSlide();
}

function goToSlide(index) {
  slideManager.goToSlide(index);
}

function autoSlide() {
  const delay =
    parseInt(document.querySelector("#slider").dataset.delay) * 1000 || 5000;
  autoSlideInterval = setInterval(() => slideManager.nextSlide(), delay);
}
