/**
 * Cloudflare image CDN helper for static HTML pages.
 * Override by setting window.IMAGE_CDN before this script loads.
 */
(function () {
  var CDN = window.IMAGE_CDN || 'https://cdn.westsummerlinhomes.com';

  window.IMAGE_CDN = CDN;

  window.cdnImage = function (path) {
    var normalized = path.charAt(0) === '/' ? path : '/' + path;
    return CDN + normalized;
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
