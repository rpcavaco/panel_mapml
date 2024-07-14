const LAYERURL_PRE = 'https://web-geoserver.ccdr-n.pt/geoserver/geoapp/wms?bbox={xmin},{ymin},{xmax},{ymax}&format=image%2Fpng&service=WMS&request=GetMap&srs=EPSG%3A3857&width={w}&height={h}&layers=';
const LAYERURL_POST = '&transparent=true&version=1.1.1&styles=';

/**
 * Finds all elements in the entire page matching `selector`, even if they are in shadowRoots.
 * Just like `querySelectorAll`, but automatically expand on all child `shadowRoot` elements.
 * @see https://stackoverflow.com/a/71692555/2228771
 */
function querySelectorAllShadows(selector, el = document.body) {
    // recurse on childShadows
    const childShadows = Array.from(el.querySelectorAll('*')).
      map(el => el.shadowRoot).filter(Boolean);
  
    const childResults = childShadows.map(child => querySelectorAllShadows(selector, child));
    
    // fuse all results into singular, flat array
    const result = Array.from(el.querySelectorAll(selector));
    return result.concat(childResults).flat();
}

/**
 * MapML  Helper to add a new layer to map
 * @param {*} p_mapvel - mapview element
 * @param {*} layertitle - layer name for TOC
 * @param {*} layername - wms layer name
 * @param {*} xmin - bounding box xmin in Web Mercator EPSG 3857
 * @param {*} ymin - bounding box ymin in Web Mercator EPSG 3857
 * @param {*} xmax - bounding box xmax in Web Mercator EPSG 3857
 * @param {*} ymax - bounding box ymax in Web Mercator EPSG 3857
 */
function addNewLayer(p_mapvel, layertitle, layername, xmin, ymin, xmax, ymax) {

    // find previously added layers
    const existing = querySelectorAllShadows('#dynamic-layer');

    // removing each previously added layer
    if (existing.length > 0) {

        let found = false;
        for (let el of existing) {

            // if layer to add already exists , found = true
            if (el.dataset.title == layertitle) {
                found = true;
                continue;
            }

            el.parentNode.removeChild(el);
        }

        // if layer to add already exists , return
        if (found) {
            return;
        }
     
    }
  
    const l = document.createElement('layer-');
    l.setAttribute('id', 'dynamic-layer');
    l.dataset.title = layertitle;
    l.checked = 'true';
    p_mapvel.appendChild(l);

    // <map-meta name="extent" content="top-left-easting=-967000, top-left-northing=5036000, bottom-right-easting=-940000, bottom-right-northing=5011800"></map-meta>

    const mm = document.createElement('map-meta');
    mm.name = 'extent';
    mm.content = `top-left-easting=${xmin}, top-left-northing=${ymax}, bottom-right-easting=${xmax}, bottom-right-northing=${ymin}`;
    l.appendChild(mm);
  
      //alert(mm.content);
  
    const mt = document.createElement('map-title');
    mt.innerText = layertitle;
    l.appendChild(mt);

    const me = document.createElement('map-extent');
    me.setAttribute('units', 'OSMTILE');
    me.setAttribute('checked','true');
    l.appendChild(me);

    const mi = document.createElement('map-input');
    mi.name = 'z';
    mi.type = 'zoom';
    mi.value = '18';
    mi.min = '4';
    mi.max = '18';
    me.appendChild(mi);

    const mi1 = document.createElement('map-input');
    mi1.setAttribute('name','w');
    mi1.setAttribute('type','width');
    me.appendChild(mi1);

    const mi2 = document.createElement('map-input');
    mi2.setAttribute('name','h');
    mi2.setAttribute('type','height');
    me.appendChild(mi2);

    const mi3 = document.createElement('map-input');
    mi3.name = 'xmin';
    mi3.type = 'location';
    mi3.units = 'pcrs';
    mi3.position = 'top-left';
    mi3.axis = 'easting';
    me.appendChild(mi3);  

    const mi4 = document.createElement('map-input');
    mi4.name = 'ymin';
    mi4.type = 'location';
    mi4.units = 'pcrs';
    mi4.position = 'bottom-right';
    mi4.axis = 'northing';
    me.appendChild(mi4);  
  
    const mi5 = document.createElement('map-input');
    mi5.name = 'xmax';
    mi5.type = 'location';
    mi5.units = 'pcrs';
    mi5.position = 'bottom-right';
    mi5.axis = 'easting';
    me.appendChild(mi5);  

    const mi6 = document.createElement('map-input');
    mi6.name = 'ymax';
    mi6.type = 'location';
    mi6.units = 'pcrs';
    mi6.position = 'top-left';
    mi6.axis = 'northing';
    me.appendChild(mi6);  

    const x = LAYERURL_PRE + layername + LAYERURL_POST;
  
    const ml = document.createElement('map-link');
    ml.setAttribute('rel', 'image');
    ml.setAttribute('tref', x);
    me.appendChild(ml);  
  
      /* <map-title>REN VNG</map-title>
      <map-extent units="OSMTILE"  checked>
          <map-input name="z" type="zoom" value="18" min="4" max="18"></map-input>
          <map-input name="w" type="width"></map-input>
          <map-input name="h" type="height"></map-input>
          <map-input name="xmin" type="location" units="pcrs" position="top-left" axis="easting" ></map-input>
          <map-input name="ymin" type="location" units="pcrs" position="bottom-left" axis="northing" ></map-input>
          <map-input name="xmax" type="location" units="pcrs" position="top-right" axis="easting" ></map-input>
          <map-input name="ymax" type="location" units="pcrs" position="top-left" axis="northing" ></map-input>
          <map-link rel="image" tref="https://web-geoserver.ccdr-n.pt/geoserver/geoapp/wms?bbox={xmin},{ymin},{xmax},{ymax}&format=image%2Fpng&service=WMS&request=GetMap&srs=EPSG%3A3857&width={w}&height={h}&layers=REN_VNG&transparent=true&version=1.1.1&styles="/>
      </map-extent>      */
}
  
