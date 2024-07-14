# import pandas as pd
import panel as pn
import psycopg2
import codecs
import json

DEBUG_MODE = False

js_files = {
    'app': 'assets/app.js'
}
js_modules = {
    'mapml': 'assets/node_modules/@maps4html/web-map-custom-element/dist/mapml-viewer.js'
}
pn.extension(js_files=js_files, js_modules=js_modules)

btn_code = """
if (op.value.length < 2) {
    alert('Must select a municpality before refreshing');
    return;
}
      
let maps = querySelectorAllShadows('mapml-viewer');
maps[0].zoomTo(lat.text, long.text, zoom.value);

addNewLayer(maps[0], "REN " + op.value, wmslyr.text, xmin.text, ymin.text, xmax.text, ymax.text);
"""

button = pn.widgets.Button(name="Refresh", icon="refresh", button_type="primary")

rawdata = {}
with codecs.open("/home/app/assets/municip_data_final.json", "r", encoding="utf-8") as fp_md:
        rawdata = json.load(fp_md)

autocomplete = pn.widgets.AutocompleteInput(
    options=list(rawdata.keys()),
    case_sensitive=False, search_strategy='includes',
    placeholder='start writing here ..')

# tZoom = pn.widgets.TextInput(value='12', visible=DEBUG_MODE)
tZoom = pn.widgets.IntSlider(name="Zoom level", value=8, start=0, end=18)

tLat = pn.widgets.StaticText(value='0', width=10, visible=DEBUG_MODE)
tLong = pn.widgets.StaticText(value='0', width=10, visible=DEBUG_MODE)

tXmin = pn.widgets.StaticText(value='0', width=10, visible=DEBUG_MODE)
tYmin = pn.widgets.StaticText(value='0', width=10, visible=DEBUG_MODE)
tXmax = pn.widgets.StaticText(value='0', width=10, visible=DEBUG_MODE)
tYmax = pn.widgets.StaticText(value='0', width=10, visible=DEBUG_MODE)
tWMSLyr = pn.widgets.StaticText(value='0', width=10, visible=DEBUG_MODE)

def ac_callback(event):
    if event.new in rawdata.keys():
        tLat.value = rawdata[event.new]['lat']
        tLong.value = rawdata[event.new]['lon']
        tXmin.value = rawdata[event.new]['xmin']
        tYmin.value = rawdata[event.new]['ymin']
        tXmax.value = rawdata[event.new]['xmax']
        tYmax.value = rawdata[event.new]['ymax']
        tWMSLyr.value = rawdata[event.new]['wmslayer']

watcher = autocomplete.param.watch(ac_callback, ['value'], onlychanged=True)

button.jscallback(clicks=btn_code, args={'op': autocomplete, 'lat': tLat, 'long': tLong, 'zoom': tZoom, 'xmin': tXmin, 'ymin': tYmin, 'xmax': tXmax, 'ymax': tYmax, 'wmslyr': tWMSLyr})

leftcol = pn.Column('## Choose a municipality', autocomplete, tZoom, tLat, tLong, tXmin, tYmin, tXmax, tYmax, tWMSLyr, button, height=100)

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



template = pn.template.BootstrapTemplate(title='REN at North')

template.sidebar.append(leftcol)
template.main.append("# National Ecological Reserve, Northern Portugal")
template.main.append(map_pane)
template.servable();