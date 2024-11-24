import time
import folium
from jinja2 import Template
from branca.element import MacroElement
import pandas as pd
import numpy as np
from streamlit_folium import folium_static, st_folium
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import streamlit_imagegrid
import plotly.graph_objects as go

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
def animate1():
    # Add a slider to choose the number of icons
    num_icons = st.slider("Select number of icons", min_value=1, max_value=20, value=10)

    # Random positions for icons
    x_positions = np.random.uniform(0, 10, num_icons)  # Random X positions
    y_positions = np.random.uniform(0, 10, num_icons)  # Random Y positions

    # Random fade-in start times for each icon (between 0 and 10)
    start_times = np.random.uniform(0, 10, num_icons)  # Random start times between 0 and 10
    fade_duration = 15  # Duration for fade-in effect (in frames)
    num_frames = 120  # Total number of frames in the animation (increased for smoother transitions)

    # Create the figure
    fig = go.Figure()

    # List to store frame data
    frames_data = []

    # Text icon (for example, using the "person" emoji)
    icon_text = "👤"

    # Generate the frames
    for frame_number in range(1, num_frames + 1):
        icons = []  # List to store icon settings for the current frame

        # Calculate opacity for each icon
        for i in range(num_icons):
            # Calculate opacity: fade in after start time
            if frame_number >= start_times[i]:
                fade_in_progress = min(1, (frame_number - start_times[i]) / fade_duration)
            else:
                fade_in_progress = 0  # Keep opacity 0 if the fade hasn't started

            # Add icon settings for this frame (using Scatter for text markers)
            icons.append(go.Scatter(
                x=[x_positions[i]],  # X position
                y=[y_positions[i]],  # Y position
                text=[icon_text],  # Text to display (the "icon")
                mode='text',  # Mode as text
                textfont=dict(size=20, color="black"),  # Text font size and color
                opacity=fade_in_progress,  # Dynamic opacity for fade-in
                showlegend=False  # Hide legend for icons
            ))

        # Create a frame with the icons
        frames_data.append(go.Frame(
            data=icons,  # Add icons with their opacity for this frame
            name=f"Frame {frame_number}"
        ))

    # Update layout for the figure
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
        xaxis=dict(
            showline=False,
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showline=False,
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        title="Text Icon Fade-In Animation",
        sliders=[{
            'currentvalue': {
                'visible': False  # Hide slider
            },
        }],
        autosize=True  # Automatically size the plot
    )

    # Add frames to the figure
    fig.frames = frames_data

    # Update the layout to autoplay the animation as soon as the slider is changed (no buttons)
    fig.update_layout(
        updatemenus=[],  # No buttons displayed
        sliders=[]  # Remove the slider visibility from here
    )

    # Update the frame duration to make the animation smoother
    frame_duration = 1000 / 60  # 60 FPS (reduce to 1000ms / 60fps for smoothness)

    # Display the figure in Streamlit
    st.plotly_chart(fig)
def animate():
    # Streamlit app title
    st.title("Animated Person Icons Appearing with Random Start Times")

    # Slider to control population size
    population = st.slider("Set the population", min_value=1, max_value=100, value=50)

    # Generate data for the animation
    num_icons = population  # Set number of icons based on population
    frames = np.arange(1, num_icons + 1)  # Each frame adds one more person icon
    x_positions = np.random.uniform(0, 10, num_icons)  # Random x positions for icons
    y_positions = np.random.uniform(0, 10, num_icons)  # Random y positions for icons

    # Random fade-in start times for each icon (between 0 and max frames)
    start_times = np.random.uniform(1, 10, num_icons)  # Random start times for each icon
    fade_duration = 10  # Duration of fade-in effect (same for all icons)

    # Create a DataFrame for positions and frame data
    df = pd.DataFrame({
        'x': x_positions,
        'y': y_positions,
        'frame': frames
    })

    # Create a plotly figure for the animated person icons
    fig = go.Figure()

    # Add person icons (using Unicode characters 👤 for person)
    for i in range(num_icons):
        fig.add_trace(go.Scatter(  # Using scatter for animation
            x=[x_positions[i]],
            y=[y_positions[i]],
            mode="markers+text",
            text=["👤"],  # Unicode character for a person
            textposition="middle center",
            marker=dict(size=30, color='rgba(0, 128, 0, 0.7)', opacity=0),
            showlegend=False,
            name=f"Person {i + 1}",
            hoverinfo="none"
        ))

    # Update layout to make it clean
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        xaxis=dict(
            showline=False,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            title=None
        ),
        yaxis=dict(
            showline=False,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            title=None
        ),
        title="Animated Person Icons Appearing with Random Start Times"
    )

    # Create frames to simulate the fade-in effect with random start times and same duration
    frames_data = []
    num_frames = 1000

    # Generate more intermediate frames for smoother transition
    for i in range(1, num_frames + 1):
        frame_data = df.iloc[:num_icons]  # Take all icons for this frame

        opacity_frame = []  # Initialize opacity list for this frame

        # For each icon, calculate the opacity based on its start time and fade duration
        for j in range(num_icons):
            # Only start fading in after the random start time
            if i >= start_times[j]:
                # Calculate opacity as the current frame progresses from start time to end
                fade_in_progress = min(1, (i - start_times[j] + 1) / fade_duration)  # Ensure opacity doesn't exceed 1
            else:
                fade_in_progress = 0  # If the frame hasn't reached the start time, keep it invisible

            opacity_frame.append(fade_in_progress)

        # Create the frame with updated opacities
        frames_data.append(go.Frame(
            data=[go.Scatter(  # Using scatter for animation
                x=frame_data['x'],
                y=frame_data['y'],
                mode="markers+text",
                text=["👤"] * num_icons,
                textposition="middle center",
                marker=dict(size=30, color='rgba(0, 128, 0, 0.7)', opacity=opacity_frame),
                showlegend=False,
                name=f"Person {i}",
                hoverinfo="none"
            )],
            name=f"Frame {i}"
        ))

    # Add frames to the figure
    fig.frames = frames_data

    # Set up animation to autoplay
    fig.update_layout(
        # Set up animation to autoplay
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(
                label="Play",
                method="animate",
                args=[None, dict(
                    frame=dict(duration=0, redraw=True),  # Faster frame duration for higher frame rate
                    fromcurrent=True,
                    mode="immediate",  # Start immediately
                    transition=dict(duration=0)  # No transition between frames
                )]
            )]
        )],
    )

    # Display the animated figure
    st.plotly_chart(fig)

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
        height: 250px;  /* Fixed height for scrolling */
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
    popup_content += '''<div class="popup-container"><div class="main-popup">'''
    popup_content += f"<h3><strong>{title}</strong></h3>"
    popup_content += f"<p>{text}</p>"
    # for im_link in image_links:
    #     popup_content += f"<br><image width='250' height='180' controls><source src='{im_link}' type='image/{video_format}'></image><br>"
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

def display_kpi_metrics(kpis, kpi_names):
    st.subheader("KPI Metrics")
    m = len(kpis)
    for i, (col, (kpi_name, kpi_value)) in enumerate(zip(st.columns(m), zip(kpi_names, kpis))):
        col.metric(label=kpi_name, value=kpi_value)

st.set_page_config(page_title= "MadCowMap" , page_icon='https://github.com/b-teh/map-testing/blob/main/MadCow.png?raw=true', layout='wide')
st.title("MadCowMap")


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
# st.markdown("""<style>
#     .stMultiSelect div[role="listbox"] {
#         position: absolute;
#         top: 45px;  /* Adjust this value to move it below the search bar */
#         z-index: 1000;
#     }
#     </style>""", unsafe_allow_html=True)


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
        popup_content = create_popup(row.Latitude, row.Longitude,row.Location, row.Description, [], [])
        #     popup_content += return_stats_html([lat,long]) #add statistics
        popup = folium.Popup(popup_content, max_width=300)
        customicon = folium.features.CustomIcon(f"{row.Project}CircleHighlighted.png",icon_size=(30, 30))
        fg.add_child(folium.Marker(location=[row.Latitude, row.Longitude],
                                   popup=popup,
                                   icon=customicon,
                                   tooltip=f'{row.Location}'
        ))
        #now add in details to c

#create container with video and description
with st.container():
    col1, col2 = st.columns([3,2])
    with col1:
        map_component = st_folium(m, width=800, height=500, feature_group_to_add=fg)#, feature_group_to_add=fg
        st.session_state.selected_id = map_component['last_object_clicked_tooltip']
    with col2:
        if st.session_state.selected_id is not None:
            st.subheader(st.session_state.selected_id)
            # st.markdown(f"""<h2 style="font-family: 'Roboto', sans-serif;
            #      color: black;
            #      padding: 1.5% 1% 1.5% 3.5%;">
            #         {st.session_state.selected_id}
            #     </h2>""", unsafe_allow_html=True)
            st.write(df.loc[df.Location == st.session_state.selected_id,'Description'].iloc[0])
            # st.markdown(f"""<p style="font-family: 'Arial', sans-serif;
            #      color: Black;
            #      padding: 1.5% 1% 1.5% 3.5%;">
            #         {df.loc[df.Location == st.session_state.selected_id,'Description'].iloc[0]}
            #     </p>""", unsafe_allow_html=True)
            st.video(data=video_url)
            a,b,c = st.columns([1,1,1])
            with b:
                st.button('Random Button')


#create popups
# h,d =
dances = ['<blockquote class="tiktok-embed" cite="https://www.tiktok.com/@yuki_dance_/video/7306857516044979457" data-video-id="7306857516044979457" style="max-width: 605px;min-width: 325px;" > <section> <a target="_blank" title="@yuki_dance_" href="https://www.tiktok.com/@yuki_dance_?refer=embed">@yuki_dance_</a> When you have friends that are willing to do crazy things with you 🤣 <a title="หลวงพี่แจ๊ส4g" target="_blank" href="https://www.tiktok.com/tag/%E0%B8%AB%E0%B8%A5%E0%B8%A7%E0%B8%87%E0%B8%9E%E0%B8%B5%E0%B9%88%E0%B9%81%E0%B8%88%E0%B9%8A%E0%B8%AA4g?refer=embed">#หลวงพี่แจ๊ส4g</a> <a title="หลวงพี่" target="_blank" href="https://www.tiktok.com/tag/%E0%B8%AB%E0%B8%A5%E0%B8%A7%E0%B8%87%E0%B8%9E%E0%B8%B5%E0%B9%88?refer=embed">#หลวงพี่</a> <a title="danceinpublic" target="_blank" href="https://www.tiktok.com/tag/danceinpublic?refer=embed">#danceinpublic</a> <a title="goyoung" target="_blank" href="https://www.tiktok.com/tag/goyoung?refer=embed">#goyoung</a> <a title="dancechallenge" target="_blank" href="https://www.tiktok.com/tag/dancechallenge?refer=embed">#dancechallenge</a> <a target="_blank" title="♬ original sound  - Yuki Dance" href="https://www.tiktok.com/music/original-sound-Yuki-Dance-7306857549872155393?refer=embed">♬ original sound  - Yuki Dance</a> </section> </blockquote> <script async src="https://www.tiktok.com/embed.js"></script>',
          '<blockquote class="tiktok-embed" cite="https://www.tiktok.com/@urbanverbunk/video/7438991737575492886" data-video-id="7438991737575492886" style="max-width: 605px;min-width: 325px;" > <section> <a target="_blank" title="@urbanverbunk" href="https://www.tiktok.com/@urbanverbunk?refer=embed">@urbanverbunk</a> RIYADH STREETS 🇸🇦🌃 We took our dance to downtown Riyadh to see how the locals would like it. We even got a little help from them!  @عثمان  @Sherine Abdelwahab  <a title="riyadh" target="_blank" href="https://www.tiktok.com/tag/riyadh?refer=embed">#riyadh</a> <a title="olayastreets" target="_blank" href="https://www.tiktok.com/tag/olayastreets?refer=embed">#olayastreets</a> <a title="localriyadh" target="_blank" href="https://www.tiktok.com/tag/localriyadh?refer=embed">#localriyadh</a> <a title="sherine" target="_blank" href="https://www.tiktok.com/tag/sherine?refer=embed">#sherine</a> <a title="sherineremix" target="_blank" href="https://www.tiktok.com/tag/sherineremix?refer=embed">#sherineremix</a> <a title="sabryaalil" target="_blank" href="https://www.tiktok.com/tag/sabryaalil?refer=embed">#sabryaalil</a> <a title="sherinesabryaalil" target="_blank" href="https://www.tiktok.com/tag/sherinesabryaalil?refer=embed">#sherinesabryaalil</a> <a title="urbanverbunk" target="_blank" href="https://www.tiktok.com/tag/urbanverbunk?refer=embed">#urbanverbunk</a> <a title="uv" target="_blank" href="https://www.tiktok.com/tag/uv?refer=embed">#uv</a> <a title="arabsgottalent" target="_blank" href="https://www.tiktok.com/tag/arabsgottalent?refer=embed">#arabsgottalent</a> <a title="riyadh" target="_blank" href="https://www.tiktok.com/tag/riyadh?refer=embed">#riyadh</a> <a title="saudiarabia" target="_blank" href="https://www.tiktok.com/tag/saudiarabia?refer=embed">#saudiarabia</a> <a title="folkdance" target="_blank" href="https://www.tiktok.com/tag/folkdance?refer=embed">#folkdance</a> <a title="streetdance" target="_blank" href="https://www.tiktok.com/tag/streetdance?refer=embed">#streetdance</a> <a title="urbandance" target="_blank" href="https://www.tiktok.com/tag/urbandance?refer=embed">#urbandance</a> <a title="reels" target="_blank" href="https://www.tiktok.com/tag/reels?refer=embed">#reels</a> <a title="dance" target="_blank" href="https://www.tiktok.com/tag/dance?refer=embed">#dance</a> <a target="_blank" title="♬ Sabry Aalil - Sherine" href="https://www.tiktok.com/music/Sabry-Aalil-6969056894707042306?refer=embed">♬ Sabry Aalil - Sherine</a> </section> </blockquote> <script async src="https://www.tiktok.com/embed.js"></script>']
with st.expander('Flashmob'):
    for dance in dances:
        st.components.v1.html(dance, height=600)
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
    data = pd.DataFrame(abs(np.random.randn(24, 3)),columns = ['Youths','Middle Aged','Seniors'])

    tab1.subheader("Hourly foot traffic")
    tab1.bar_chart(data)
with tab2:
    budget = st.slider("Select a budget value", min_value=0, max_value = 100, value = 50)
    text1 = "Calculating Outreach"
    text2 = "Sourcing Productions"
    bar1 = st.progress(0, text=text1)
    bar2 = st.progress(0, text=text2)
    prog_rate = np.random.uniform(0.01,0.03)
    k = np.random.uniform(1.5,2)
    for i in range(101):
        bar1.progress(min(int(k*i),100), text =text1 )
        bar2.progress(i, text=text2)
        time.sleep(prog_rate)

    bar1.empty()
    bar2.empty()

    st.header("Project Details Dashboard")
    def calc_metrics(budg):
        manhours = round(budg*50.718)
        productions = max(int(budg/25),1)
        pax = round(budg*11.245)
        return [str(pax)+' Pax',str(productions)+' Productions' ,str(manhours)+' Mins']
    metrics = calc_metrics(budget)
    metric_names = ['Expected Outreach', 'Exhibits','Engagement']
    c = st.columns(len(metrics))
    for i in range(len(metrics)):
        c[i].metric(label = metric_names[i], value = metrics[i])
    style_metric_cards(background_color = "#FA8072", border_left_color="#F83C28")


# st.markdown("""
#     <style>
#         .custom-header {
#             margin-top: 20px;  # Adjust this value to control the vertical spacing
#         }
#     </style>
# """, unsafe_allow_html=True)
# st.markdown("""
#             <style>
#                    .block-container {
#                         padding-top: 1rem;
#                         padding-bottom: 0rem;
#                         padding-left: 3rem;
#                         padding-right: 3rem;
#                     }
#             </style>
#             """, unsafe_allow_html=True)


