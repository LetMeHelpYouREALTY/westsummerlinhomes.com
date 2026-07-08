(function () {
  document.querySelectorAll('.nav-toggle').forEach(function (button) {
    var nav = document.getElementById(button.getAttribute('aria-controls') || '');
    if (!nav) {
      return;
    }

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
})();
