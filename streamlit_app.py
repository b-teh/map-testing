import folium
from jinja2 import Template
from branca.element import MacroElement
import pandas as pd
import numpy as np
from streamlit_folium import folium_static, st_folium
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import streamlit_imagegrid

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
# Define the HTML for the web video
video_url = "https://www.youtube.com/watch?v=Ht_ab1Wov3E"  # Sample MP4 video link
video_format = 'mp4'
logo_url = "https://github.com/b-teh/map-testing/blob/main/MadCow.png?raw=true"
projects = ['Mowe']
TITLE = 'MadCowMap'

@st.cache_data
def load_df():
    #change code to load data accordingly
    df = pd.read_csv('locations.csv')
    return df

def init_map(center=(1.352, 103.8198), zoom_start=13, map_type="OpenStreetMap"):
    return folium.Map(location=center, zoom_start=zoom_start, tiles=map_type)

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

def create_popup(lat,lng,title, text, image_links=[], video_links=[]):
    popup_content = return_style_html()
    popup_content += '''<div class="popup-container">
    <div class="main-popup">'''
    popup_content += f"<h3><strong>{title}</strong></h3>"
    popup_content += f"<p>{text}</p>"
    for im_link in image_links:
        popup_content += f"<br><image width='250' height='180' controls><source src='{im_link}' type='image/{video_format}'></image><br>"
    # for vid_link in video_links:
    #     popup_content += f"""
    #         <iframe width="320" height="240"
    #         src="{video_url}" frameborder="0"
    #         allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
    #         </iframe>
    #     """
    popup_content += f'''<a href=https://www.google.com/maps?layer=c&cbll={lat},{lng}  target=blank> Street View</a>
'''
    # popup_content += f'''<button onclick="document.getElementById('innerPopup').style.display='block';">Show Statistics</button>
    # <div id="innerPopup"  style="display:none;" class="inner-popup">
    #     <h4>Key Statistics</h4>''' + generate_stats_images([0, 0]) + f'''<button onclick="document.getElementById('innerPopup').style.display='none';">Close</button>
    # </div>'''
    popup_content += '''</div></div>'''  # closing the div containers
    return popup_content

def add_project(df, custom_logo, project_name,folium_map):
    # Layer 1
    project_1 = folium.FeatureGroup(name=project_name)
    for idx, row in df.iterrows():
        popup_content = create_popup(row.Latitude, row.Longitude,row.Location, row.Description, [], [video_url])
        # popup_content += return_stats_html([row.Latitude,row.Longitude]) #add statistics
        popup = folium.Popup(popup_content, max_width=300)
        customicon = folium.features.CustomIcon(custom_logo, icon_size=(30, 30))
        folium.Marker(location=[row['Latitude'], row['Longitude']],
                      icon=customicon,
                      popup = popup,
                      tooltip=f'{row.Location}').add_to(folium_map)
        # project_1.add_to(m)
    return folium_map

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
    #class="fa-solid fa-3x fa-street-view
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
        html: '<i class="fa-solid fa-3x fa-street-view" /i>',
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
        new_mark.bindPopup("<a href=https://www.google.com/maps?layer=c&cbll=" + lat + "," + lng + " target=blank> Street View</a>");
        parent.document.getElementById("latitude").value = lat;
        parent.document.getElementById("longitude").value =lng;
        };
        {{this._parent.get_name()}}.on('click', newMarker);
    {% endmacro %}
    """)  # noqa

    def __init__(self, popup=None):
        super(ClickForOneMarker, self).__init__(popup)
        self._name = 'ClickForOneMarker'

# @st.cache_data  # @st.cache_data
def load_map():
    # Load the map
    map = init_map()  # init
    df = load_df()
    # # Multi-select widget to allow users to choose which markers to highlight
    for proj in projects:
        add_project(df[df['Project'] == proj], f"{proj}Circle.png" ,proj,map)

    return map

st.set_page_config(page_title= "MadCowMap" , page_icon='MadCow.png', layout='wide')
#Set title
st.markdown("")
st.markdown(f"""
    <div style="display: flex; align-items: center;">
    <img src = "{logo_url}" style="width: 50px; height: 50px; margin-right: 20px;">
    <h1 style="text-align: left; font-family: 'Abadi', sans-serif; color: #000000;">
        {TITLE}
    </h1>
    </div>
    <hr style="border: 2px solid #000000; width: 100%; margin: 0px auto;  margin-left: 0px;">
""", unsafe_allow_html=True)


# if 'map_center' not in st.session_state:
#     st.session_state.map_center = [1.352, 103.8198]
#     st.session_state.zoom_level =  13

# onemap_tile_url = "	https://www.onemap.gov.sg/maps/tiles/Night_HD/{z}/{x}/{y}.png"
# Initialize session state for selected markers
if "selected_labels" not in st.session_state:
    st.session_state.selected_labels = []

# Initialize session state if it's not already initialized
if "selection_order" not in st.session_state:
    st.session_state.selection_order = []
df = load_df()
#create multiselection
with st.sidebar:
    selected_labels = st.multiselect(
        "Select Locations",
        options=df["Location"],
        default=st.session_state.selection_order,  # Default to the recorded order
    )
#adjust multiselection location
st.markdown("""<style>
    .stMultiSelect div[role="listbox"] {
        position: absolute;
        top: 45px;  /* Adjust this value to move it below the search bar */
        z-index: 1000;
    }
    </style>""", unsafe_allow_html=True)


m = load_map()
#init of selected location
if "selected_id" not in st.session_state:
    st.session_state.selected_id = None

# Create a div to inject the menu directly into the map
m.get_root().html.add_child(folium.Element(menu_content))
folium.LayerControl().add_to(m)
click_for_marker = ClickForOneMarker()
m.add_child(click_for_marker)

# Refresh for marker selection to highlight
fg = folium.FeatureGroup(name="Markers")
for _, row in df.iterrows():
    # Determine marker color based on whether it is selected or not
    # Add the marker with custom popup and color
    if row["Location"] in selected_labels:
        popup_content = create_popup(row['Location'], row['Description'], [], [video_url])
        #     popup_content += return_stats_html([lat,long]) #add statistics
        popup = folium.Popup(popup_content, max_width=300)
        customicon = folium.features.CustomIcon(f"{row.Project}CircleHighlighted.png",icon_size=(30, 30))
        fg.add_child(folium.Marker(location=[row.Latitude, row.Longitude],
                                   popup=popup,
                                   icon=customicon,
                                   tooltip=f'{row.Location}'
        ))
        #now add in details to c

# st.markdown("""
#         <style>
#             .rounded-box {
#                 border-radius: 15px;
#                 padding: 20px;
#                 background-color: #00008B;  # Turquoise color
#                 color: #ffffff;  # White text color for better contrast
#                 box-shadow: 6px 6px 12px rgba(0, 0, 0, 0.3), -6px -6px 12px rgba(255, 255, 255, 0.5);  # Bevel effect
#                 max-width: 100%;
#         </style>
#     """, unsafe_allow_html=True)



#create container with video and description
with st.container():
    col1, col2 = st.columns([2,3])
    with col2:
        map_component = st_folium(m, width=800, height=500, feature_group_to_add=fg)#, feature_group_to_add=fg
        st.session_state.selected_id = map_component['last_object_clicked_tooltip']
    with col1:
        with stylable_container(
            key="container_with_border",
            css_styles="""
                {
                    border-radius: 0.5rem;
                    padding: 100 px;
                    background-color: #00008B;
                    box-shadow: 6px 6px 12px rgba(0, 0, 0, 0.3), -6px -6px 12px rgba(255, 255, 255, 0.5);
                }
                """,
        ):
            if st.session_state.selected_id is not None:
                st.markdown(f"""
                    <h2 style="font-family: 'Roboto', sans-serif;
                     color: white;
                     padding: 1.5% 1% 1.5% 3.5%;">
                        {st.session_state.selected_id}
                    </h2>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                    <p style="font-family: 'Arial', sans-serif;
                     color: white;
                     padding: 1.5% 1% 1.5% 3.5%;">
                        {df.loc[df.Location == st.session_state.selected_id,'Description'].iloc[0]}
                    </p>
                """, unsafe_allow_html=True)
                st.video(data=video_url)
                a,b,c = st.columns([1,1,1])
                with b:
                    st.button('textsdfsdfdgfddfgf')
                st.markdown("")
    st.markdown("""
        <style>
            .stTabs>div { margin-top: 0px; }  /* Remove margin between the sections */
        </style>
    """, unsafe_allow_html=True)
#create popups
with st.expander('Flashmob'):
    st.write('here')
pre = 'C:/Users/brand/OneDrive/Documents/Portfolio Documents/Marketing/'
image_urls = [
    'https://github.com/b-teh/map-testing/blob/main/IMG-20241112-WA0010.jpg?raw=true',
    'https://github.com/b-teh/map-testing/blob/main/IMG-20241112-WA0011.jpg?raw=true',
    'https://github.com/b-teh/map-testing/blob/main/IMG-20241112-WA0013.jpg?raw=true',
    'https://github.com/b-teh/map-testing/blob/main/IMG-20241112-WA0014.jpg?raw=true',
    'https://github.com/b-teh/map-testing/blob/main/IMG-20241112-WA0015.jpg?raw=true',
]
n = len(image_urls)
n_cols = 3
i = 0
with st.expander('Larger than Life'):
    cols =st.columns(n_cols)
    for im in image_urls:
        with cols[i]:
            st.image(im)
        i = (i+1)%n_cols

# # Initialize session state variables for the index
# if "current_index" not in st.session_state:
#     st.session_state.current_index = 0  # Index of the first image in the current set of images
#
# if "disable_next" not in st.session_state:
#     st.session_state.disable_next = False
# if "disable_back" not in st.session_state:
#     st.session_state.disable_back = True
# # Number of images to display per page
# images_per_page = 3
#
# def update_vals():
#     st.session_state['disable_back'] = (st.session_state.current_index<= 3)
#     st.session_state['disable_next'] = ((st.session_state.current_index + images_per_page +3)>= len(image_urls))
# disable_back = (st.session_state.current_index <= 0)
# disable_next = (st.session_state.current_index + images_per_page >= len(image_urls))
# with st.expander('Larger Than Life'):
#     back_col, display1, display2, display3, next_col = st.columns([1.5,4,4,4,1.5])
#     # Check if we are at the beginning or end of the list
#
#     # Add images inside the scrollable container
#     with back_col:
#         if st.button("←", on_click=update_vals,disabled = disable_back):
#             st.session_state.current_index -=3
#     with next_col:
#         if st.button("→", on_click=update_vals, disabled = disable_next):
#             st.session_state.current_index +=3
#     st.write(st.session_state.current_index)
#     disable_back = (st.session_state.current_index <= 0)
#     disable_next = (st.session_state.current_index + images_per_page >= len(image_urls))
#     with display1:
#         st.image(image_urls[st.session_state.current_index])
#         st.write('A brief description')
#     with display2:
#         if st.session_state.current_index +1<n:
#             st.image(image_urls[st.session_state.current_index+1])
#             st.write('A brief description')
#             end_idx = st.session_state.current_index + 1
#     with display3:
#         if st.session_state.current_index +2<n:
#             st.image(image_urls[st.session_state.current_index+2])
#             st.write('A brief description')
#             end_idx = st.session_state.current_index +2
#
#     # Display the current index (optional)
#     st.write(f"Showing collections {st.session_state.current_index+1} to {end_idx+1} of {len(image_urls)}")
with st.container():
    tab1, tab2, tab3 = st.tabs(["Pax Show-up Profile", "Project Outreach", "Temp"])
    data = pd.DataFrame(abs(np.random.randn(10, 3)),columns = ['Youths','Middle Aged','Seniors'])

    tab1.subheader("A tab with a chart")
    tab1.bar_chart(data)
with tab2:
    budget = st.slider("Select a budget value", min_value=0, max_value = 100, value = 50)

st.markdown("""
    <style>
        .custom-header {
            margin-top: 20px;  # Adjust this value to control the vertical spacing
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
            <style>
                   .block-container {
                        padding-top: 1rem;
                        padding-bottom: 0rem;
                        padding-left: 3rem;
                        padding-right: 3rem;
                    }
            </style>
            """, unsafe_allow_html=True)
