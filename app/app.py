# import pandas as pd
import panel as pn
import psycopg2

from functools import partial

DEBUG_MODE = True

js_modules = {
    'mapml': 'assets/node_modules/@maps4html/web-map-custom-element/dist/mapml-viewer.js'
}
pn.extension(js_modules=js_modules)

btn_code = """
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

alert(op.value + ' ' + lat.text + ' ' + long.text + ' ' + zoom.value);
//alert(p_municip, data);

let maps = querySelectorAllShadows('mapml-viewer');
maps[0].zoomTo(lat.text,long.text, zoom.value);
"""

button = pn.widgets.Button(name="Refresh", icon="refresh", button_type="primary")

rawdata = {}
with psycopg2.connect("host=10.0.2.2 dbname=basedata user=basedata password=basedata") as conn:

    with conn.cursor() as cur:

        cur.execute("""select concelho as nome, st_y(geom) as lat, st_x(geom) as lon
            from (
                select concelho, st_transform(st_centroid(geom), 4326) geom
                from caop.v_concelhos_rn 
                order by concelho
            ) a""")
        for row in cur.fetchall():
            rawdata[row[0]] = [row[1], row[2]]


autocomplete = pn.widgets.AutocompleteInput(
    options=list(rawdata.keys()),
    case_sensitive=False, search_strategy='includes',
    placeholder='start writing here ..')

tZoom = pn.widgets.TextInput(value='12', visible=DEBUG_MODE)
tLat = pn.widgets.StaticText(value='0', width=10, visible=DEBUG_MODE)
tLong = pn.widgets.StaticText(value='0', width=10, visible=DEBUG_MODE)


def ac_callback(event):
    if event.new in rawdata.keys():
        tLat.value = rawdata[event.new][0]
        tLong.value = rawdata[event.new][1]
 
watcher = autocomplete.param.watch(ac_callback, ['value'], onlychanged=True)

#button.js_on_click(args={'p_municip': 'xx' }, code=btn_code)

button.jscallback(clicks=btn_code, args={'op': autocomplete, 'lat': tLat, 'long': tLong, 'zoom': tZoom})


# data = pd.DataFrame(rawdata)

leftcol = pn.Column('## Choose a municipality', autocomplete, tZoom, tLat, tLong, button, height=100)

mappane_styles = {
    'background-color': '#F6F6F6'
}
map_pane = pn.pane.HTML("""
<mapml-viewer projection="OSMTILE" zoom="8" lat="41.38" lon="-7.66" height="700" width="900" controls> 
    <layer- label="OpenStreetMap" checked>
        <map-extent units="OSMTILE" checked>
            <map-input name="z" type="zoom"  value="18" min="0" max="18"></map-input>
            <map-input name="x" type="location" units="tilematrix" axis="column" min="0"  max="262144" ></map-input>
            <map-input name="y" type="location" units="tilematrix" axis="row" min="0"  max="262144" ></map-input>
            <map-link rel="tile" tref="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png" ></map-link>
        </map-extent>
    </layer->
</mapml-viewer> 
""", styles=mappane_styles)

flexb = pn.Row(leftcol, map_pane)


pn.Column("# National Ecological Reserve, Northern Portugal", flexb).servable()