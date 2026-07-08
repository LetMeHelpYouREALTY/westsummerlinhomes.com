(function () {
  var CALENDLY_URL = 'https://calendly.com/drjanduffy/in-person-real-estate-consultation';
  var WIDGET_JS = 'https://assets.calendly.com/assets/external/widget.js';
  var WIDGET_CSS = 'https://assets.calendly.com/assets/external/widget.css';
  var loadPromise = null;

  function loadCalendlyAssets() {
    if (loadPromise) {
      return loadPromise;
    }

    loadPromise = new Promise(function (resolve, reject) {
      if (!document.querySelector('link[data-calendly-css="true"]')) {
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = WIDGET_CSS;
        link.dataset.calendlyCss = 'true';
        document.head.appendChild(link);
      }

      if (window.Calendly) {
        resolve();
        return;
      }

      var script = document.createElement('script');
      script.src = WIDGET_JS;
      script.async = true;
      script.dataset.calendlyJs = 'true';
      script.onload = function () {
        resolve();
      };
      script.onerror = reject;
      document.body.appendChild(script);
    });

    return loadPromise;
  }

  function initCalendly() {
    if (!window.Calendly) {
      return;
    }

    Calendly.initBadgeWidget({
      url: CALENDLY_URL,
      text: 'Schedule time with me',
      color: '#ffffff',
      textColor: '#0a2540',
      branding: false,
    });

    document.querySelectorAll('.calendly-popup').forEach(function (el) {
      if (el.dataset.calendlyBound === 'true') {
        return;
      }
      el.dataset.calendlyBound = 'true';
      el.addEventListener('click', openCalendlyPopup);
    });
  }

  function openCalendlyPopup(event) {
    if (event) {
      event.preventDefault();
    }

    loadCalendlyAssets()
      .then(function () {
        initCalendly();
        if (window.Calendly) {
          Calendly.initPopupWidget({ url: CALENDLY_URL });
        }
      })
      .catch(function () {
        window.location.href = 'contact.html';
      });
  }

  window.openCalendlyPopup = openCalendlyPopup;

  var inlineWidgets = document.querySelectorAll('.calendly-inline-widget');
  if (inlineWidgets.length) {
    var inlineObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) {
            return;
          }
          loadCalendlyAssets()
            .then(initCalendly)
            .catch(function () {
              /* Contact page still has phone/email fallback */
            });
          inlineObserver.disconnect();
        });
      },
      { rootMargin: '120px 0px', threshold: 0.01 }
    );

    inlineWidgets.forEach(function (widget) {
      inlineObserver.observe(widget);
    });
  } else if ('requestIdleCallback' in window) {
    requestIdleCallback(function () {
      loadCalendlyAssets().then(initCalendly).catch(function () {});
    });
  }
})();
