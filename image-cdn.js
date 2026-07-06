/**
 * Image URL helper for static HTML pages.
 * Uses local /images/ by default; set window.IMAGE_CDN before load for Cloudflare.
 */
(function () {
  var CDN = window.IMAGE_CDN || '';

  window.cdnImage = function (path) {
    var normalized = path.charAt(0) === '/' ? path : '/' + path;
    return CDN ? CDN.replace(/\/$/, '') + normalized : normalized;
  };

  window.siteImages = {
    hero: window.cdnImage('/images/hero-bg.jpg'),
    og: window.cdnImage('/images/og-image.jpg'),
    agent: window.cdnImage('/images/dr-janet-duffy.jpg'),
    agentOg: window.cdnImage('/images/dr-janet-duffy-real-estate.jpg'),
    logo: window.cdnImage('/images/logo.png'),
    property: function (n) {
      return window.cdnImage('/images/property-' + n + '.jpg');
    },
    testimonial: function (n) {
      return window.cdnImage('/images/testimonial-' + n + '.jpg');
    },
  };
})();
