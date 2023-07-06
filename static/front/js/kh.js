document.addEventListener('DOMContentLoaded', function() {
    const prevButton = document.querySelector('.prev-btn');
    const nextButton = document.querySelector('.next-btn');
    const slider = document.querySelector('.slider');
    const slides = document.querySelectorAll('.slider img');
    const dots = document.querySelectorAll('.dot');
    let currentIndex = 0;
  
    function showSlide(index) {
      slider.style.transform = `translateX(-${index * 100}%)`;
      dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
      });
    }
  
    prevButton.addEventListener('click', function() {
      currentIndex = (currentIndex - 1 + slides.length) % slides.length;
      showSlide(currentIndex);
    });
  
    nextButton.addEventListener('click', function() {
      currentIndex = (currentIndex + 1) % slides.length;
      showSlide(currentIndex);
    });
  
    dots.forEach((dot, i) => {
      dot.addEventListener('click', function() {
        currentIndex = i;
        showSlide(currentIndex);
      });
    });
  });