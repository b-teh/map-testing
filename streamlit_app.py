import time

import folium
from jinja2 import Template
from branca.element import MacroElement
import pandas as pd
from streamlit_folium import folium_static, st_folium
import streamlit as st
from streamlit_sortables import sort_items

menu_content = """
<style>
    #menu {
        position: absolute;
        top: 10px;
        left: 50px;
        z-index: 1000;
        background-color: #f9f9f9;
        border: 2px solid #007BFF;
        border-radius: 5px;
        padding: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    #menu h3 {
        color: #007BFF;
        margin: 0;
    }
    #menu ul {
        list-style-type: none;
        padding: 0;
    }
    #menu li {
        padding: 5px 0;
    }
    #menu button {
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 15px;
        cursor: pointer;
        font-size: 16px;
    }
    #menu button:hover {
        background-color: #0056b3;
    }
    .hidden {
        display: none;
    }
</style>
<div id="menu">
    <button id="menuButton" onclick="toggleMenu()">Show Menu</button>
    <div id="menuOptions" class="hidden">
        <h3>Menu Options</h3>
        <ul>
            <li>Option 1: Dance Venues</li>
            <li>Option 2: General Campaign Locations</li>
            <li>Option 3: Larger than Life Selection</li>
        </ul>
    </div>
</div>

<script>
function toggleMenu() {
    var menuOptions = document.getElementById('menuOptions');
    var button = document.getElementById('menuButton');
    if (menuOptions.classList.contains('hidden')) {
        menuOptions.classList.remove('hidden');
        button.innerHTML = 'Hide Menu';
    } else {
        menuOptions.classList.add('hidden');
        button.innerHTML = 'Show Menu';
    }
}
</script>
"""
def generate_stats_images(location):
    #to insert code
    stats_file1 = 'average-hourly-footfall-by-day-of-the-week.png'
    stats_file2 = 'other_stats.png'
    stats_html = ''
    stats_html +=f'''<img src="{stats_file1}" alt="Footfall" style="width:100%; height:auto;">'''
    stats_html +=f'''<img src="{stats_file2}" alt="Footfall" style="width:100%; height:auto;">'''
    return stats_html

def return_style_html():
    style_html = '''<style>
    .popup-container {
        font-family: Arial, sans-serif;
        height: 300px;  /* Fixed height for scrolling */
        overflow-y: auto;  /* Enable vertical scrolling */
        text-align: left;
    }
    .main-popup h3 {
        color: #007BFF;
    }
    .main-popup button, .inner-popup button {
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 12px;
        cursor: pointer;
        font-size: 14px;
        margin-top: 10px;
    }
    .main-popup button:hover, .inner-popup button:hover {
        background-color: #0056b3;
    }
    .inner-popup {
        padding: 10px;
        border: 1px solid #007BFF;
        background-color: #f9f9f9;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        display: none; /* Start hidden */
    }
</style>'''
    return style_html

def create_popup(title, text, image_links=[], video_links=[]):
    popup_content = return_style_html()
    popup_content += '''<div class="popup-container">
    <div class="main-popup">'''
    popup_content += f"<h3><strong>{title}</strong></h3>"
    popup_content += f"<p>{text}</p>"
    for im_link in image_links:
        popup_content += f"<br><image width='250' height='180' controls><source src='{im_link}' type='image/{video_format}'></image><br>"
    for vid_link in video_links:
        popup_content += f"""
            <iframe width="320" height="240" 
            src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
            </iframe>
        """
    popup_content += f'''<button onclick="document.getElementById('innerPopup').style.display='block';">Show Statistics</button>
    <div id="innerPopup"  style="display:none;" class="inner-popup">
        <h4>Key Statistics</h4>''' + generate_stats_images([0, 0]) + f'''<button onclick="document.getElementById('innerPopup').style.display='none';">Close</button>
    </div>'''
    popup_content += '''</div></div>'''  # closing the div containers
    return popup_content

def add_project(df, custom_logo, project_name):
    # Layer 1
    project_1 = folium.FeatureGroup(name=project_name)
    for idx, row in df.iterrows():
        title, lat, long, write_up = row['Location'], row['Latitude'], row['Longitude'], row['Description']
        popup_content = create_popup(title, write_up, [], [video_url])
        #     popup_content += return_stats_html([lat,long]) #add statistics
        popup = folium.Popup(popup_content, max_width=300)
        customicon = folium.features.CustomIcon(custom_logo, icon_size=(30, 30))
        folium.Marker(location=[lat, long], popup=popup, icon=customicon).add_to(project_1)
        project_1.add_to(m)
    #     m.get_root().html.add_child(folium.Element(f"""
    #     <script>
    #         var marker = L.marker([{lat}, {long}]).addTo(m);
    #
    #         // Add click event listener to marker
    #         marker.on('click', function() {{
    #             marker._icon.style.transition = 'box-shadow 0.5s ease-in-out';
    #             marker._icon.style.boxShadow = '0 0 15px 5px rgba(0, 255, 255, 0.8)';  // Glow effect
    #
    #         }});
    #     </script>
    # """))

class ClickForOneMarker(folium.ClickForMarker):
    """
    Description of the tool
    """
    _template = Template(u"""
    {% macro header(this,kwargs) %}
        <style>
            .StreetViewIcon{
                color: green;
            }
        </style>
    {% endmacro %}
    {% macro script(this, kwargs) %}
        const fontAwesomeIcon = L.divIcon({
        html: '<i class="fa-solid fa-3x fa-street-view"></i> ',
        iconSize: [0,0],
        iconAnchor:[15,0],
        className: 'StreetViewIcon'
        });
        var new_mark = L.marker();
        function newMarker(e){
        new_mark.setLatLng(e.latlng).addTo({{this._parent.get_name()}});
        new_mark.setIcon(fontAwesomeIcon)
        new_mark.dragging.enable();
        new_mark.on('dblclick', function(e){ {{this._parent.get_name()}}.removeLayer(e.target)})
        var lat = e.latlng.lat.toFixed(4),
        lng = e.latlng.lng.toFixed(4);
        new_mark.bindPopup("<a href=https://www.google.com/maps?layer=c&cbll=" + lat + "," + lng + " target=blank ><img src=streetview.png width=30></img> Street View</a>");
        parent.document.getElementById("latitude").value = lat;
        parent.document.getElementById("longitude").value =lng;
        };
        {{this._parent.get_name()}}.on('click', newMarker);
    {% endmacro %}
    """)  # noqa

    def __init__(self, popup=None):
        super(ClickForOneMarker, self).__init__(popup)
        self._name = 'ClickForOneMarker'

if 'map_center' not in st.session_state:
    st.session_state.map_center = [1.352, 103.8198]
    st.session_state.zoom_level =  13
# Create a map centered at a specific latitude and longitude
m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom_level)
# onemap_tile_url = "	https://www.onemap.gov.sg/maps/tiles/Night_HD/{z}/{x}/{y}.png"
# Initialize session state for selected markers
if "selected_labels" not in st.session_state:
    st.session_state.selected_labels = []

# Define the HTML for the web video
video_url = "C:/Users/brand/OneDrive/Documents/Portfolio Documents/Marketing/300_DL.mp4"  # Sample MP4 video link
video_format = 'mp4'
df = pd.read_csv('locations.csv')
projects = ['Chanel', 'Dior']
for proj in projects:
    add_project(df[df['Project'] == proj], f"{proj}Circle.png" ,proj)

# Initialize session state if it's not already initialized
if "selection_order" not in st.session_state:
    st.session_state.selection_order = []

#adjust multiselection location
st.markdown("""
    <style>
    .stMultiSelect div[role="listbox"] {
        position: absolute;
        top: 45px;  /* Adjust this value to move it below the search bar */
        z-index: 1000;
    }
    </style>
""", unsafe_allow_html=True)

# Multi-select widget to allow users to choose which markers to highlight
with st.sidebar:
    selected_labels = st.multiselect(
        "Select Locations",
        options=df["Location"],
        default=st.session_state.selection_order,  # Default to the recorded order
    )

# Create a div to inject the menu directly into the map
m.get_root().html.add_child(folium.Element(menu_content))
folium.LayerControl().add_to(m)
click_for_marker = ClickForOneMarker()
m.add_child(click_for_marker)

fg = folium.FeatureGroup(name="Markers")
for _, row in df.iterrows():
    # Determine marker color based on whether it is selected or not
    # Add the marker with custom popup and color
    if row["Location"] in selected_labels:
        popup_content = create_popup(row['Location'], row['Description'], [], [video_url])
        #     popup_content += return_stats_html([lat,long]) #add statistics
        popup = folium.Popup(popup_content, max_width=300)
        customicon = folium.features.CustomIcon(f"{row['Project']}CircleHighlighted.png",icon_size=(30, 30))
        fg.add_child(folium.Marker(location=[row['Latitude'], row['Longitude']],
                                   popup=popup,
                                   icon=customicon
        ))




sorted_items = sort_items(st.session_state.selected_labels)

# Render the Folium map in Streamlit
map_component = st_folium(m, width=800, height=500, key='new', feature_group_to_add=fg)

