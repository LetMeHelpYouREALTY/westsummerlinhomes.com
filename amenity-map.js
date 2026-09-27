(function () {
  'use strict';

  var CONFIG = window.WEST_SUMMERLIN_AMENITY_CONFIG;
  if (!CONFIG) {
    return;
  }

  var mapsConfigPromise = null;
  var mapsReady = null;
  var categorySearchCache = new Map();

  var mapsAuthFailed = false;
  if (typeof window !== 'undefined') {
    window.addEventListener('gmaps:auth-failure', function () {
      mapsAuthFailed = true;
    });
  }

  function fetchMapsConfig() {
    if (mapsConfigPromise) {
      return mapsConfigPromise;
    }
    mapsConfigPromise = fetch('/api/maps-config', { credentials: 'same-origin' })
      .then(function (res) {
        if (!res.ok) {
          return { apiKey: '', mapId: '' };
        }
        return res.json();
      })
      .catch(function () {
        return { apiKey: '', mapId: '' };
      });
    return mapsConfigPromise;
  }

  function loadGoogleMaps(apiKey) {
    if (typeof window === 'undefined') {
      return Promise.reject(new Error('ssr'));
    }
    if (window.google && window.google.maps && typeof window.google.maps.importLibrary === 'function') {
      return Promise.resolve();
    }
    if (mapsReady) {
      return mapsReady;
    }
    mapsReady = new Promise(function (resolve, reject) {
      var cb = '__gmapsReady';
      window[cb] = function () {
        resolve();
      };
      window.gm_authFailure = function () {
        window.dispatchEvent(new Event('gmaps:auth-failure'));
        reject(new Error('gm_authFailure'));
      };
      var script = document.createElement('script');
      script.src =
        'https://maps.googleapis.com/maps/api/js?key=' +
        encodeURIComponent(apiKey) +
        '&v=weekly&loading=async&callback=' +
        cb;
      script.async = true;
      script.onerror = function () {
        mapsReady = null;
        reject(new Error('maps script failed'));
      };
      document.head.appendChild(script);
    });
    return mapsReady;
  }

  function searchCategoryPlaces(center, categoryId, types) {
    var cached = categorySearchCache.get(categoryId);
    if (cached) {
      return cached;
    }
    var promise = google.maps
      .importLibrary('places')
      .then(function (placesLib) {
        var Place = placesLib.Place;
        return Place.searchNearby({
          fields: ['displayName', 'location', 'formattedAddress', 'googleMapsURI', 'id'],
          locationRestriction: {
            center: center,
            radius: CONFIG.searchRadiusMeters,
          },
          includedPrimaryTypes: types,
          maxResultCount: 10,
          rankPreference: 'POPULARITY',
        });
      })
      .then(function (response) {
        return response.places || [];
      });
    promise.catch(function () {
      categorySearchCache.delete(categoryId);
    });
    categorySearchCache.set(categoryId, promise);
    return promise;
  }

  function embedFallbackUrl(center) {
    return (
      'https://www.google.com/maps?q=' +
      encodeURIComponent(center.lat + ',' + center.lng) +
      '&z=14&output=embed'
    );
  }

  function directionsUrl(place) {
    if (place.googleMapsURI) {
      return place.googleMapsURI;
    }
    if (place.placeId) {
      return (
        'https://www.google.com/maps/dir/?api=1&destination_place_id=' +
        encodeURIComponent(place.placeId)
      );
    }
    var dest =
      place.lat != null && place.lng != null
        ? place.lat + ',' + place.lng
        : encodeURIComponent(place.address || place.name);
    return 'https://www.google.com/maps/dir/?api=1&destination=' + dest;
  }

  function escapeHtml(str) {
    return String(str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function buildStaticListHtml(categoryId) {
    var items = CONFIG.staticAmenities.filter(function (item) {
      return !categoryId || item.category === categoryId;
    });
    if (!items.length) {
      items = CONFIG.staticAmenities;
    }
    var list = items
      .map(function (item) {
        var href = item.sourceUrl || 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(item.name + ', ' + item.address);
        var addrLine = item.address ? ' — ' + escapeHtml(item.address) : '';
        return (
          '<li><a href="' +
          escapeHtml(href) +
          '" target="_blank" rel="noopener noreferrer">' +
          escapeHtml(item.name) +
          '</a>' +
          addrLine +
          '</li>'
        );
      })
      .join('');
    return (
      '<div class="amenity-map-static-list" aria-label="Featured nearby places">' +
      '<h3>Featured places near West Summerlin</h3>' +
      '<ul>' +
      list +
      '</ul></div>'
    );
  }

  function updateStaticList(root, categoryId) {
    var panel = root.querySelector('.amenity-map-panel');
    if (!panel) {
      return;
    }
    var existing = root.querySelector('.amenity-map-static-list');
    var html = buildStaticListHtml(categoryId);
    if (existing) {
      existing.outerHTML = html;
    } else {
      panel.insertAdjacentHTML('beforeend', html);
    }
  }

  function renderFallback(root, categoryId, message) {
    var center = CONFIG.community.center;
    var canvasWrap = root.querySelector('.amenity-map-canvas-wrap');
    if (!canvasWrap) {
      return;
    }
    canvasWrap.innerHTML =
      '<iframe title="Map of West Summerlin, Las Vegas" src="' +
      embedFallbackUrl(center) +
      '" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>';
    var status = root.querySelector('.amenity-map-status');
    if (status) {
      status.textContent =
        message ||
        'Interactive map loads when a Google Maps API key is configured. Showing map preview and featured locations.';
    }
    updateStaticList(root, categoryId);
  }

  function AmenityMapWidget(root) {
    this.root = root;
    this.compact = root.classList.contains('amenity-map-compact');
    this.map = null;
    this.markers = [];
    this.infoWindow = null;
    this.communityMarker = null;
    this.activeCategory = CONFIG.categoryOrder[0];
    this.mapId = '';
    this.initialized = false;
    this.fallbackMode = false;
    this.authFailureHandler = null;
  }

  AmenityMapWidget.prototype.bindAuthFailureListener = function () {
    var self = this;
    if (this.authFailureHandler) {
      return;
    }
    this.authFailureHandler = function () {
      self.switchToFallback('Map preview and featured locations are shown while interactive maps are unavailable.');
    };
    window.addEventListener('gmaps:auth-failure', this.authFailureHandler);
  };

  AmenityMapWidget.prototype.unbindAuthFailureListener = function () {
    if (this.authFailureHandler) {
      window.removeEventListener('gmaps:auth-failure', this.authFailureHandler);
      this.authFailureHandler = null;
    }
  };

  AmenityMapWidget.prototype.switchToFallback = function (message) {
    if (this.fallbackMode) {
      return;
    }
    this.fallbackMode = true;
    this.teardownInteractiveMap();
    renderFallback(this.root, this.activeCategory, message);
  };

  AmenityMapWidget.prototype.teardownInteractiveMap = function () {
    this.clearMarkers();
    if (this.communityMarker && this.communityMarker.map) {
      this.communityMarker.map = null;
    }
    this.communityMarker = null;
    if (this.infoWindow) {
      this.infoWindow.close();
    }
    this.map = null;
    var canvasWrap = this.root.querySelector('.amenity-map-canvas-wrap');
    if (canvasWrap) {
      canvasWrap.innerHTML =
        '<iframe title="Map of West Summerlin, Las Vegas" src="' +
        embedFallbackUrl(CONFIG.community.center) +
        '" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>';
    }
  };

  AmenityMapWidget.prototype.buildShell = function () {
    var filters = CONFIG.categoryOrder
      .map(function (id) {
        var cat = CONFIG.categories[id];
        return (
          '<button type="button" class="amenity-map-filter" data-category="' +
          id +
          '" aria-pressed="false" aria-label="Show ' +
          escapeHtml(cat.label) +
          ' near West Summerlin">' +
          escapeHtml(cat.label) +
          '</button>'
        );
      })
      .join('');

    this.root.innerHTML =
      '<div class="amenity-map-panel" role="region" aria-label="Nearby amenities map for West Summerlin">' +
      '<div class="amenity-map-filters" role="toolbar" aria-label="Amenity categories">' +
      filters +
      '</div>' +
      '<div class="amenity-map-canvas-wrap">' +
      '<div class="amenity-map-canvas" aria-hidden="true"></div>' +
      '</div>' +
      '<p class="amenity-map-status" aria-live="polite">Loading map…</p>' +
      (this.compact ? '' : buildStaticListHtml(this.activeCategory)) +
      '</div>';

    var self = this;
    this.root.querySelectorAll('.amenity-map-filter').forEach(function (btn) {
      btn.addEventListener('click', function () {
        self.setCategory(btn.getAttribute('data-category'));
      });
    });
    this.setCategory(this.activeCategory, true);
  };

  AmenityMapWidget.prototype.setCategory = function (categoryId, skipSearch) {
    this.activeCategory = categoryId;
    this.root.querySelectorAll('.amenity-map-filter').forEach(function (btn) {
      var active = btn.getAttribute('data-category') === categoryId;
      btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    if (this.fallbackMode) {
      updateStaticList(this.root, categoryId);
      return;
    }
    if (!skipSearch && this.map) {
      this.searchCategory(categoryId);
    }
  };

  AmenityMapWidget.prototype.clearMarkers = function () {
    this.markers.forEach(function (m) {
      if (m.setMap) {
        m.setMap(null);
      }
      if (m.map) {
        m.map = null;
      }
    });
    this.markers = [];
  };

  AmenityMapWidget.prototype.addCommunityMarker = function () {
    var center = CONFIG.community.center;
    var self = this;
    var position = { lat: center.lat, lng: center.lng };
    var title = CONFIG.community.markerTitle;

    if (this.mapId && window.google.maps.marker && window.google.maps.marker.AdvancedMarkerElement) {
      var pin = document.createElement('div');
      pin.className = 'amenity-community-pin';
      pin.textContent = '★';
      pin.setAttribute('aria-hidden', 'true');
      pin.style.cssText =
        'background:#0a2540;color:#c9a227;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;border:2px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,.25)';
      this.communityMarker = new google.maps.marker.AdvancedMarkerElement({
        map: this.map,
        position: position,
        title: title,
        content: pin,
      });
    } else {
      this.communityMarker = new google.maps.Marker({
        map: this.map,
        position: position,
        title: title,
        zIndex: 999,
      });
    }

    this.communityMarker.addListener('click', function () {
      self.openInfo({
        name: CONFIG.community.name,
        address: 'West Summerlin, ' + CONFIG.community.city + ', ' + CONFIG.community.region,
        lat: center.lat,
        lng: center.lng,
      });
    });
  };

  AmenityMapWidget.prototype.openInfo = function (place) {
    if (!this.infoWindow) {
      this.infoWindow = new google.maps.InfoWindow();
    }
    var wrap = document.createElement('div');
    wrap.style.maxWidth = '220px';
    var titleEl = document.createElement('strong');
    titleEl.textContent = place.name || 'Place';
    wrap.appendChild(titleEl);
    if (place.address) {
      var addr = document.createElement('p');
      addr.style.margin = '0.25rem 0';
      addr.textContent = place.address;
      wrap.appendChild(addr);
    }
    var link = document.createElement('p');
    link.style.margin = '0.5rem 0 0';
    var a = document.createElement('a');
    a.href = directionsUrl(place);
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.textContent = 'Directions';
    link.appendChild(a);
    wrap.appendChild(link);
    this.infoWindow.setContent(wrap);
    if (place.lat != null && place.lng != null) {
      this.infoWindow.setPosition({ lat: place.lat, lng: place.lng });
      this.infoWindow.open(this.map);
    }
  };

  AmenityMapWidget.prototype.placeToMarkerData = function (place) {
    var lat;
    var lng;
    if (place.location) {
      if (typeof place.location.toJSON === 'function') {
        var json = place.location.toJSON();
        lat = json.lat;
        lng = json.lng;
      } else {
        lat = typeof place.location.lat === 'function' ? place.location.lat() : place.location.lat;
        lng = typeof place.location.lng === 'function' ? place.location.lng() : place.location.lng;
      }
    }
    var displayName = place.displayName;
    if (displayName && typeof displayName === 'object' && displayName.text) {
      displayName = displayName.text;
    }
    return {
      name: displayName || place.name || 'Place',
      address: place.formattedAddress || place.vicinity || '',
      lat: lat,
      lng: lng,
      placeId: place.id || place.place_id,
      googleMapsURI: place.googleMapsURI,
    };
  };

  AmenityMapWidget.prototype.addPlaceMarker = function (data) {
    if (data.lat == null || data.lng == null) {
      return;
    }
    var self = this;
    var marker = new google.maps.Marker({
      map: this.map,
      position: { lat: data.lat, lng: data.lng },
      title: data.name,
    });
    marker.addListener('click', function () {
      self.openInfo(data);
    });
    this.markers.push(marker);
  };

  AmenityMapWidget.prototype.searchCategory = function (categoryId) {
    var self = this;
    var cat = CONFIG.categories[categoryId];
    var status = this.root.querySelector('.amenity-map-status');
    if (!cat || !this.map || this.fallbackMode) {
      return;
    }
    if (status) {
      status.textContent = 'Searching for ' + cat.label.toLowerCase() + ' near West Summerlin…';
    }
    this.clearMarkers();
    this.addCommunityMarker();

    var center = CONFIG.community.center;
    var types = cat.primaryTypes.slice();

    function showCuratedFallback() {
      updateStaticList(self.root, categoryId);
      if (status) {
        status.textContent =
          'Showing featured ' + cat.label.toLowerCase() + ' near West Summerlin (see list below).';
      }
    }

    searchCategoryPlaces(center, categoryId, types)
      .then(function (places) {
        if (self.fallbackMode) {
          return;
        }
        places.forEach(function (p) {
          self.addPlaceMarker(self.placeToMarkerData(p));
        });
        if (status) {
          status.textContent =
            places.length > 0
              ? 'Showing ' + places.length + ' ' + cat.label.toLowerCase() + ' near West Summerlin.'
              : 'No ' + cat.label.toLowerCase() + ' results in this radius. See featured places below.';
        }
        if (!places.length) {
          showCuratedFallback();
        }
      })
      .catch(function () {
        if (self.fallbackMode) {
          return;
        }
        showCuratedFallback();
      });
  };

  AmenityMapWidget.prototype.initInteractive = function (apiKey, mapId) {
    var self = this;
    this.mapId = mapId || '';
    return loadGoogleMaps(apiKey)
      .then(function () {
        if (mapId) {
          return google.maps.importLibrary('marker');
        }
        return null;
      })
      .then(function () {
        var canvas = self.root.querySelector('.amenity-map-canvas');
        if (!canvas || self.fallbackMode) {
          return;
        }
        var mapOpts = {
          center: CONFIG.community.center,
          zoom: CONFIG.community.zoom,
          mapTypeControl: false,
          streetViewControl: false,
          fullscreenControl: true,
        };
        if (mapId) {
          mapOpts.mapId = mapId;
        }
        self.map = new google.maps.Map(canvas, mapOpts);
        self.addCommunityMarker();
        self.searchCategory(self.activeCategory);
        self.initialized = true;
      });
  };

  AmenityMapWidget.prototype.init = function () {
    if (this.initialized) {
      return;
    }
    this.buildShell();
    this.bindAuthFailureListener();
    var self = this;

    if (mapsAuthFailed) {
      renderFallback(self.root, self.activeCategory);
      self.fallbackMode = true;
      return;
    }

    fetchMapsConfig().then(function (cfg) {
      var key = (cfg && cfg.apiKey) || '';
      if (!key || mapsAuthFailed) {
        renderFallback(self.root, self.activeCategory);
        self.fallbackMode = true;
        return;
      }
      self
        .initInteractive(key, cfg.mapId)
        .catch(function () {
          self.switchToFallback('Map could not load. Showing preview and featured locations.');
        });
    });
  };

  AmenityMapWidget.prototype.destroy = function () {
    this.unbindAuthFailureListener();
    this.teardownInteractiveMap();
  };

  function observeWidget(el) {
    var widget = new AmenityMapWidget(el);
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            observer.disconnect();
            widget.init();
          }
        });
      },
      { rootMargin: '120px 0px', threshold: 0.05 }
    );
    observer.observe(el);
  }

  function boot() {
    document.querySelectorAll('.amenity-map-widget').forEach(observeWidget);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
