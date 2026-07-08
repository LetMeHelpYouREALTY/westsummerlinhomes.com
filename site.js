(function () {
  // Mobile nav toggle
  document.querySelectorAll('.nav-toggle').forEach(function (button) {
    var nav = document.getElementById(button.getAttribute('aria-controls') || '');
    if (!nav) return;

    button.addEventListener('click', function () {
      var isOpen = nav.classList.toggle('is-open');
      button.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      button.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
    });

    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        nav.classList.remove('is-open');
        button.setAttribute('aria-expanded', 'false');
        button.setAttribute('aria-label', 'Open menu');
      });
    });
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var target = document.querySelector(anchor.getAttribute('href'));
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  // Header background on scroll
  var header = document.querySelector('header');
  if (header) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 80) {
        header.style.background = 'rgba(44, 62, 80, 0.97)';
      } else {
        header.style.background = '';
      }
    });
  }

  // Fade-in on scroll
  var fadeObserver = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  document.querySelectorAll('.fade-in').forEach(function (el) {
    fadeObserver.observe(el);
  });
})();
