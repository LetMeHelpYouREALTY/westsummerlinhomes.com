(function () {
  var REALSCOUT_SRC = 'https://em.realscout.com/widgets/realscout-web-components.umd.js';
  var loadPromise = null;

  function loadRealScout() {
    if (loadPromise) {
      return loadPromise;
    }

    loadPromise = new Promise(function (resolve, reject) {
      if (document.querySelector('script[data-realscout-loader="true"]')) {
        resolve();
        return;
      }

      var script = document.createElement('script');
      script.src = REALSCOUT_SRC;
      script.type = 'module';
      script.async = true;
      script.dataset.realscoutLoader = 'true';
      script.onload = function () {
        resolve();
      };
      script.onerror = reject;
      document.head.appendChild(script);
    });

    return loadPromise;
  }

  var widgets = document.querySelectorAll(
    'realscout-office-listings, realscout-advanced-search, realscout-home-value'
  );

  if (!widgets.length) {
    return;
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) {
          return;
        }
        loadRealScout().catch(function () {
          /* Widget host handles empty state if script fails */
        });
        observer.disconnect();
      });
    },
    { rootMargin: '240px 0px', threshold: 0.01 }
  );

  widgets.forEach(function (widget) {
    observer.observe(widget);
  });
})();
