/*!
 * Image Map Resizer
 * Responsive image map library
 * https://github.com/davidjbradshaw/image-map-resizer
 */

(function() {
  "use strict";

  /**
   * Resizes a single image map
   * @param {HTMLMapElement} map
   */
  function resizeMap(map) {
    // Grab all areas in the map
    const areas = map.getElementsByTagName("area");
    const coords = Array.from(areas).map(formatCoords);
    const img = getImage(map);

    // Prevent multiple initializations
    if (typeof map._resize === "function") return;

    map._resize = function() {
      const ratio = {
        width: img.width / img.naturalWidth,
        height: img.height / img.naturalHeight
      };

      const padding = {
        width: parseInt(getComputedStyle(img).getPropertyValue("padding-left"), 10),
        height: parseInt(getComputedStyle(img).getPropertyValue("padding-top"), 10)
      };

      areas.forEach((area, i) => {
        let toggle = 0;
        area.coords = coords[i].split(",").map(c => {
          const dim = toggle === 1 ? "width" : "height";
          toggle = 1 - toggle;
          return padding[dim] + Math.floor(Number(c) * ratio[dim]);
        }).join(",");
      });
    };

    // Listen to events
    img.addEventListener("load", map._resize, false);
    window.addEventListener("focus", map._resize, false);
    window.addEventListener("resize", debounce(map._resize, 250), false);
    window.addEventListener("readystatechange", map._resize, false);
    document.addEventListener("fullscreenchange", map._resize, false);

    // Initial resize
    if (img.width !== img.naturalWidth || img.height !== img.naturalHeight) {
      map._resize();
    }
  }

  /**
   * Get image associated with map
   * @param {HTMLMapElement} map
   * @returns {HTMLImageElement}
   */
  function getImage(map) {
    return document.querySelector(`img[usemap="#${map.name}"]`) ||
           document.querySelector(`img[usemap="${map.name}"]`);
  }

  /**
   * Format coordinates string (removes extra spaces)
   * @param {HTMLAreaElement} area
   */
  function formatCoords(area) {
    return area.coords.replace(/ *, */g, ",").replace(/ +/g, ",");
  }

  /**
   * Debounce helper
   */
  function debounce(fn, delay) {
    let timeout;
    return function() {
      clearTimeout(timeout);
      timeout = setTimeout(fn, delay);
    };
  }

  /**
   * Initialize all maps on page
   * @param {string|HTMLMapElement} selector
   */
  function imageMapResize(selector) {
    const maps = [];

    function processMap(map) {
      if (!map.tagName || map.tagName.toUpperCase() !== "MAP") {
        throw new TypeError(`Expected <MAP> tag, found <${map.tagName}>.`);
      }
      resizeMap(map);
      maps.push(map);
    }

    if (!selector || typeof selector === "string") {
      document.querySelectorAll(selector || "map").forEach(processMap);
    } else {
      processMap(selector);
    }

    return maps;
  }

  // Expose library
  if (typeof define === "function" && define.amd) {
    define([], imageMapResize);
  } else if (typeof module === "object" && typeof module.exports === "object") {
    module.exports = imageMapResize;
  } else {
    window.imageMapResize = imageMapResize;
  }

  // jQuery support
  if (window.jQuery) {
    window.jQuery.fn.imageMapResize = function() {
      return this.filter("map").each(resizeMap).end();
    };
  }

})();
