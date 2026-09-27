(function () {
  'use strict';

  var CONFIG = window.WEST_SUMMERLIN_AMENITY_CONFIG;
  if (!CONFIG) {
    return;
  }

  var mapsConfigPromise = null;

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

  function loadGoogleMapsScript(apiKey) {
    return new Promise(function (resolve, reject) {
      if (window.google && window.google.maps) {
        resolve(window.google.maps);
        return;
      }
      var callbackName = '__westSummerlinMapsInit';
      window[callbackName] = function () {
        try {
          delete window[callbackName];
        } catch (e) {
          window[callbackName] = undefined;
        }
        if (window.google && window.google.maps) {
          resolve(window.google.maps);
        } else {
          reject(new Error('Google Maps failed to initialize'));
        }
      };
      var script = document.createElement('script');
      script.async = true;
      script.defer = true;
      script.src =
        'https://maps.googleapis.com/maps/api/js?key=' +
        encodeURIComponent(apiKey) +
        '&libraries=places&loading=async&callback=' +
        callbackName;
      script.onerror = function () {
        reject(new Error('Google Maps script failed to load'));
      };
      document.head.appendChild(script);
    });
  }

  function embedFallbackUrl(center) {
    return (
      'https://www.google.com/maps?q=' +
      encodeURIComponent(center.lat + ',' + center.lng) +
      '&z=13&output=embed'
    );
  }

  function directionsUrl(place) {
    if (place.placeId) {
      return (
        'https://www.google.com/maps/dir/?api=1&destination_place_id=' +
        encodeURIComponent(place.placeId)
      );
    }
    var dest = place.lat != null && place.lng != null
      ? place.lat + ',' + place.lng
      : encodeURIComponent(place.address || place.name);
    return 'https://www.google.com/maps/dir/?api=1&destination=' + dest;
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
        var mapsQuery = encodeURIComponent(item.name + ', ' + item.address);
        return (
          '<li><a href="https://www.google.com/maps/search/?api=1&query=' +
          mapsQuery +
          '" target="_blank" rel="noopener noreferrer">' +
          escapeHtml(item.name) +
          '</a> — ' +
          escapeHtml(item.address) +
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

  function escapeHtml(str) {
    return String(str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
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
    var existingList = root.querySelector('.amenity-map-static-list');
    if (!existingList) {
      root.querySelector('.amenity-map-panel').insertAdjacentHTML(
        'beforeend',
        buildStaticListHtml(categoryId)
      );
    }
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
  }

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
    if (!skipSearch && this.map) {
      this.searchCategory(categoryId);
    }
  };

  AmenityMapWidget.prototype.clearMarkers = function () {
    this.markers.forEach(function (m) {
      if (m.setMap) {
        m.setMap(null);
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
    var ratingLine = place.rating
      ? '<p style="margin:0.25rem 0">Rating: ' + escapeHtml(String(place.rating)) + '</p>'
      : '';
    var addressLine = place.address
      ? '<p style="margin:0.25rem 0">' + escapeHtml(place.address) + '</p>'
      : '';
    var html =
      '<div style="max-width:220px">' +
      '<strong>' +
      escapeHtml(place.name) +
      '</strong>' +
      ratingLine +
      addressLine +
      '<p style="margin:0.5rem 0 0"><a href="' +
      directionsUrl(place) +
      '" target="_blank" rel="noopener noreferrer">Directions</a></p></div>';
    this.infoWindow.setContent(html);
    if (place.lat != null && place.lng != null) {
      this.infoWindow.setPosition({ lat: place.lat, lng: place.lng });
      this.infoWindow.open(this.map);
    }
  };

  AmenityMapWidget.prototype.placeToMarkerData = function (place) {
    var lat;
    var lng;
    if (place.location) {
      lat = typeof place.location.lat === 'function' ? place.location.lat() : place.location.lat;
      lng = typeof place.location.lng === 'function' ? place.location.lng() : place.location.lng;
    }
    var displayName = place.displayName;
    if (displayName && typeof displayName === 'object' && displayName.text) {
      displayName = displayName.text;
    }
    return {
      name: displayName || place.name || 'Place',
      address: place.formattedAddress || place.vicinity || '',
      rating: place.rating,
      lat: lat,
      lng: lng,
      placeId: place.id || place.place_id,
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
    if (!cat || !this.map) {
      return;
    }
    if (status) {
      status.textContent = 'Searching for ' + cat.label.toLowerCase() + ' near West Summerlin…';
    }
    this.clearMarkers();
    this.addCommunityMarker();

    var center = CONFIG.community.center;

    function done(count) {
      if (status) {
        status.textContent =
          count > 0
            ? 'Showing ' + count + ' ' + cat.label.toLowerCase() + ' near West Summerlin.'
            : 'No ' + cat.label.toLowerCase() + ' results in this radius. See featured places below.';
      }
    }

    if (google.maps.places && google.maps.places.Place && google.maps.places.Place.searchNearby) {
      var request = {
        fields: ['displayName', 'location', 'rating', 'formattedAddress', 'id'],
        locationRestriction: {
          center: center,
          radius: CONFIG.searchRadiusMeters,
        },
        includedPrimaryTypes: cat.primaryTypes.slice(0, 1),
        maxResultCount: 15,
      };
      google.maps.places.Place.searchNearby(request)
        .then(function (response) {
          var places = response.places || [];
          places.forEach(function (p) {
            self.addPlaceMarker(self.placeToMarkerData(p));
          });
          done(places.length);
        })
        .catch(function () {
          self.legacyNearbySearch(cat, done);
        });
      return;
    }

    this.legacyNearbySearch(cat, done);
  };

  AmenityMapWidget.prototype.legacyNearbySearch = function (cat, done) {
    var self = this;
    var service = new google.maps.places.PlacesService(this.map);
    service.nearbySearch(
      {
        location: CONFIG.community.center,
        radius: CONFIG.searchRadiusMeters,
        type: cat.legacyType,
      },
      function (results, status) {
        if (status !== google.maps.places.PlacesServiceStatus.OK || !results) {
          done(0);
          return;
        }
        results.slice(0, 15).forEach(function (r) {
          self.addPlaceMarker(self.placeToMarkerData(r));
        });
        done(results.length);
      }
    );
  };

  AmenityMapWidget.prototype.initInteractive = function (apiKey, mapId) {
    var self = this;
    this.mapId = mapId || '';
    return loadGoogleMapsScript(apiKey).then(function () {
      return google.maps.importLibrary('places');
    }).then(function () {
      if (mapId) {
        return google.maps.importLibrary('marker');
      }
      return null;
    }).then(function () {
      var canvas = self.root.querySelector('.amenity-map-canvas');
      if (!canvas) {
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
    var self = this;
    fetchMapsConfig().then(function (cfg) {
      var key = (cfg && cfg.apiKey) || '';
      if (!key) {
        renderFallback(self.root, self.activeCategory);
        return;
      }
      self
        .initInteractive(key, cfg.mapId)
        .catch(function () {
          renderFallback(self.root, self.activeCategory, 'Map could not load. Showing preview and featured locations.');
        });
    });
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
