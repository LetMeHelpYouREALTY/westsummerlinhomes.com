(function () {
  var CALENDLY_URL = 'https://calendly.com/drjanduffy/in-person-real-estate-consultation';

  function openCalendlyPopup(event) {
    if (event) {
      event.preventDefault();
    }
    if (window.Calendly) {
      Calendly.initPopupWidget({ url: CALENDLY_URL });
    }
  }

  function initCalendly() {
    if (!window.Calendly) {
      return;
    }

    Calendly.initBadgeWidget({
      url: CALENDLY_URL,
      text: 'Schedule time with me',
      color: '#0a2540',
      textColor: '#ffffff',
      branding: false,
    });

    document.querySelectorAll('.calendly-popup').forEach(function (el) {
      el.addEventListener('click', openCalendlyPopup);
    });
  }

  window.openCalendlyPopup = openCalendlyPopup;

  if (document.readyState === 'complete') {
    initCalendly();
  } else {
    window.addEventListener('load', initCalendly);
  }
})();
