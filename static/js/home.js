// mobile view menu toggle

const menuBtn = document.getElementById('menu-btn');
const dropdown = document.getElementById('dropdown');

menuBtn.addEventListener('click', () => {
  dropdown.classList.toggle('hidden'); // show/hide menu
});







// slider functionality
const slider = document.getElementById("slider");
      const slides = slider.children.length;
      let index = 0;

      function showSlide() {
        slider.style.transform = `translateX(-${index * 100}%)`;
      }

      function nextSlide() {
        index = (index + 1) % slides;
        showSlide();
      }

      function prevSlide() {
        index = (index - 1 + slides) % slides;
        showSlide();
      }

      // Auto slide every 4 sec
      setInterval(nextSlide, 4000);




      // Scroll animation

      

      const obeserver = new IntersectionObserver((ebtries)=>{

      })