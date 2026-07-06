/**
 * Image URL helper for static HTML pages.
 * Serves from jsDelivr (GitHub repo) so images work before Vercel redeploys /images/.
 * Override: window.IMAGE_CDN = 'https://your-cdn.com' before this script loads.
 */
(function () {
  var DEFAULT_CDN =
    'https://cdn.jsdelivr.net/gh/LetMeHelpYouREALTY/westsummerlinhomes.com@main';
  var CDN = window.IMAGE_CDN || DEFAULT_CDN;

  window.IMAGE_CDN = CDN;

  window.cdnImage = function (path) {
    var normalized = path.charAt(0) === '/' ? path : '/' + path;
    return CDN.replace(/\/$/, '') + normalized;
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
