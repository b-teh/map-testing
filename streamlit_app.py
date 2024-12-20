import time
import folium
from jinja2 import Template
from branca.element import MacroElement
import numpy as np
from streamlit_folium import st_folium
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
import plotly.graph_objects as go
import toml
# from streamlit_elements import elements, mui, html
import requests
import pandas as pd
from io import StringIO
# from types import SimpleNamespace
# from mui.dashboard import Dashboard, Editor, Card, DataGrid, Radar, Pie, Player
import gspread

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
# Create a connection object to feedback sheet
# conn = st.connection("gsheets", type=GSheetsConnection)
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
    # URL of the published Google Sheet (CSV format)
    sheet_url = st.secrets['locations_url']
    # Step 1: Get the data from the URL
    response = requests.get(sheet_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Step 2: Read the CSV content into a pandas DataFrame
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
    return df
@st.cache_data
def get_foot_traffic(locations):
    foot_traffic = dict()
    for loc in locations:
        df = pd.read_csv(f'foot traffic/{loc}.csv')
        foot_traffic[loc] = df
    return foot_traffic
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
    # Load the TOML configuration file

# Validate login function
def validate_login(username, password):
    correct_username = st.secrets['login']['username']
    correct_password = st.secrets['login']['password']

    # Check if the provided username and password match the ones in the TOML file
    return username == correct_username and password == correct_password

def login_page():
    # Title for the app
    st.title("Login")

    # Create a form for login
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button(label='Login')




    # Check credentials when the form is submitted
    if submit_button:
        if validate_login(username, password):
            st.success("Login successful! Redirecting to the main page...")
            st.session_state.logged_in = True
            return True
        else:
            st.session_state.logged_in = False
            st.error("Invalid username or password. Please try again.")
            return False

def main_page():
    # onemap_tile_url = "	https://www.onemap.gov.sg/maps/tiles/Night_HD/{z}/{x}/{y}.png"
    # Initialize session state for selected markers

    def plot_bar():
        # Generate synthetic data for hours of the day
        np.random.seed(42)
        hours = pd.date_range(start="2023-01-01 00:00", end="2023-01-01 23:00", freq="H")
        demographics = ['Youths','Middle-Aged','Seniors']
        data = pd.DataFrame({
            "Hour": hours.hour,
            demographics[0]: np.random.randint(10, 50, size=len(hours)),
            demographics[1]: np.random.randint(5, 30, size=len(hours)),
            demographics[2]: np.random.randint(20, 60, size=len(hours)),
        })
        # Create a Plotly figure
        fig = go.Figure()

        # Add stacked bars for each category
        fig.add_trace(go.Bar(
            x=data["Hour"],
            y=data[demographics[0]],
            name=demographics[0],
            marker_color="blue"
        ))
        fig.add_trace(go.Bar(
            x=data["Hour"],
            y=data[demographics[1]],
            name=demographics[1],
            marker_color="green"
        ))
        fig.add_trace(go.Bar(
            x=data["Hour"],
            y=data[demographics[2]],
            name=demographics[2],
            marker_color="red"
        ))

        # Configure the layout for stacking
        fig.update_layout(
            barmode="stack",  # Stacks bars vertically
            xaxis=dict(
                rangeslider=dict(visible=True),  # Add a range slider for zooming
                type="category",  # Treat x-axis as categories (hours)
                title="Hour of the Day"
            ),
            yaxis_title="Traffic",
            title="",
            legend_title="Categories",
            title_x=0.5  # Center the title
        )

        # Render the Plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    st.title("MadCowMap")
    if "selected_labels" not in st.session_state:
        st.session_state.selected_labels = []

    # Initialize session state if it's not already initialized
    if "selection_order" not in st.session_state:
        st.session_state.selection_order = []
    df = load_df()
    # create multiselection
    foot_traffic = get_foot_traffic(list(df.Location))
    m = load_map()

    # init of selected location
    if "selected_id" not in st.session_state:
        st.session_state.selected_id = None

    # markdown for tabs design
    st.markdown("""
    <style>
         .stTabs {
            background-color: #FFFFFF;  /* Light grey background behind the tabs */
            padding: 10px;
            border-radius: 10px;  /* Optional: Add rounded corners to the background */
        }
    	.stTabs [data-baseweb="tab-list"] {
    		gap: 0px;
        }
        .stTabs [data-baseweb="tab-highlight"] {
                display:none;
                background-color:transparent
            }
    	.stTabs [data-baseweb="tab"] {
    	    flex: 0.2;
    		height: 50px;
            white-space: pre-wrap;
    		background-color: #1d3557;
    		border-radius: 0px 0px 0px 0px;
    		gap: 0px;
    		padding-top: 10px;
    		padding-bottom: 10px;
    		padding-left: 10px;
    		padding-right:10px;
    		color: #FFFFFF; /* Set text color to white */
            font-weight: bold; /* Make the text bold */
        }

    	.stTabs [aria-selected="true"] {
      		background-color: #FFFFFF;
      		color: #1d3557;
      		border-radius: 10px 10px 10px 10px;
    	}
        .stTabs [aria-selected="false"] {
            border-radius: 10px 10px 0px 0px;  /* Rounded corners at the top */
    }

    </style>""", unsafe_allow_html=True)
    show_tabs = [True, True, False]
    all_tabs = ["Locations","Project Specifications", "Analytics"]
    used_tabs = st.tabs([all_tabs[i] for i in range(len(all_tabs)) if show_tabs[i]])

    #map tab
    if show_tabs[0]:
        with used_tabs[0]:
            # st_folium(m)
            col1, col2 = st.columns([3, 2])
            with col1:
                folium.LayerControl().add_to(m)
                click_for_marker = ClickForOneMarker()
                m.add_child(click_for_marker)

                # Refresh for marker selection to highlight
                fg = folium.FeatureGroup(name="Markers")
                for _, row in df.iterrows():
                    # Determine marker color based on whether it is selected or not
                    # Add the marker with custom popup and color
                    if row["Location"] in st.session_state.selected_labels:
                        popup_content = create_popup(row.Latitude, row.Longitude, row.Location, row.Description, [], [])
                        #     popup_content += return_stats_html([lat,long]) #add statistics
                        popup = folium.Popup(popup_content, max_width=300)
                        customicon = folium.features.CustomIcon(f"{row.Project}CircleHighlighted.png", icon_size=(30, 30))
                        fg.add_child(folium.Marker(location=[row.Latitude, row.Longitude],
                                                   popup=popup,
                                                   icon=customicon,
                                                   tooltip=f'{row.Location}'
                                                   ))
                with st.container(border = True):
                    map_component = st_folium(m, width=800, height=500, feature_group_to_add=fg)
                st.session_state.selected_id = map_component['last_object_clicked_tooltip']
            with col2:
                st.session_state.selected_labels = st.multiselect(
                    "Select Locations",
                    options=df["Location"],
                    default=st.session_state.selection_order,  # Default to the recorded order
                )
                save_selected = st.button('Save Selection')
                if save_selected:
                    with open("selected_options.txt", "w") as file:
                        file.write("\n".join(st.session_state.selected_labels))  # Save each option on a new line
                    success_message = st.success("Selected options saved successfully!")
                    time.sleep(2)  # Wait for 3 seconds
                    success_message.empty()
                if st.session_state.selected_id is not None:
                    with stylable_container(
                            key="container_with_border",
                            css_styles="""
                            {
                                border: 1px solid rgba(49, 51, 63, 0.2);
                                border-radius: 0.5rem;
                                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);  /* Shadow effect */
                                padding: calc(1em - 1px)
                            }
                            """,
                    ):
                        # Add some content inside the container
                        # st.subheader(st.session_state.selected_id)
                        # st.write(df.loc[df.Location == st.session_state.selected_id, 'Description'].iloc[0])
                        #now include the part abput the heat map
                        y = ['Mon','Tues','Wed','Thurs','Fri','Sat','Sun']
                        used_traffic = foot_traffic[st.session_state.selected_id]
                        x = used_traffic.columns[:]
                        z = used_traffic.iloc[:,:].values
                        # Create the heatmap
                        fig = go.Figure(
                            data=go.Heatmap(
                                z=z,
                                x=x,
                                y=y,
                                colorscale='Blues',
                                hoverongaps=False,  # Ensures no hover annotations for missing data
                                hovertemplate="Day: %{y}<br>Time: %{x}<br>Traffic: %{z}%<extra></extra>"  # Custom hover text
                            )
                        )
                        fig.update_layout(
                            title=f"Foot traffic for {st.session_state.selected_id}",
                            template="plotly",
                            width=400,  # Set desired width
                            height=400  # Set desired height
                        )
                        st.plotly_chart(fig)
    dances = [
'<blockquote class="tiktok-embed" cite="https://www.tiktok.com/@justmaiko/video/6842699291551599877" data-video-id="6842699291551599877" style="max-width: 605px;min-width: 325px;" > <section> <a target="_blank" title="@justmaiko" href="https://www.tiktok.com/@justmaiko?refer=embed">@justmaiko</a> yes, we got @jasonderulo to dance on the escalator with us to his song. Iconic? i think so😂🔥 @itsjonathanle @javierr <a target="_blank" title="♬ Savage Love (Laxed - Siren Beat) - Jawsh 685 &#38; Jason Derulo" href="https://www.tiktok.com/music/Savage-Love-Laxed-Siren-Beat-6825494114277100293?refer=embed">♬ Savage Love (Laxed - Siren Beat) - Jawsh 685 &#38; Jason Derulo</a> </section> </blockquote> <script async src="https://www.tiktok.com/embed.js"></script>',
'<blockquote class="tiktok-embed" cite="https://www.tiktok.com/@orchardroadfashion/video/7295287742924131591" data-video-id="7295287742924131591" style="max-width: 605px;min-width: 325px;" > <section> <a target="_blank" title="@orchardroadfashion" href="https://www.tiktok.com/@orchardroadfashion?refer=embed">@orchardroadfashion</a> “What’s your jam” with @Vin @Myra Carel @H🍯NEY @ashlie0.2 @Arthur II 🇵🇭🇸🇬  Song: 3D. Y @AB_______JK_M____RST____Y_ featuring @Jack Harlow  <a title="orchardroadfashion" target="_blank" href="https://www.tiktok.com/tag/orchardroadfashion?refer=embed">#orchardroadfashion</a> <a target="_blank" title="♬ 3D (feat. Jack Harlow) - Jung Kook &#38; Jack Harlow" href="https://www.tiktok.com/music/3D-feat-Jack-Harlow-7283427877760190466?refer=embed">♬ 3D (feat. Jack Harlow) - Jung Kook &#38; Jack Harlow</a> </section> </blockquote> <script async src="https://www.tiktok.com/embed.js"></script>']
    #project specs tab
    if show_tabs[1]:
        with used_tabs[1]:
            with st.expander('Flashmob'):
                flashmob_cols = st.columns(3)
                i=0
                for dance in dances:
                    with flashmob_cols[i]:
                        with st.container(border = True):
                            st.components.v1.html(dance, height=600)
                            i  = (i+1)%3
            pre = 'C:/Users/brand/OneDrive/Documents/Portfolio Documents/Marketing/'
            # image_urls = [
            #     '1ds53SpE-sR3UYtFjOd99rOa_0qC_BlqX',
            #     '1CJy_i3JG0v5ZbpNJhSdH3Uacktw0ULW8',
            #     '10Y5mS0uCKruzep2gVQsI-JVqAVzXqabX',
            #     '1QXW4xl5YHAd5oqdF67D3YpqUrxj0QHDY',
            #     '1pc0wVWHL_IcwFThXpfLvFJboANfsuWOv'
            # ]#google images
            image_urls = [
                'https://github.com/b-teh/map-testing/blob/main/LTL%20MOWE.jpg?raw=true',
                'https://github.com/b-teh/map-testing/blob/main/IMG-20241112-WA0015.jpg?raw=true',
                'https://github.com/b-teh/map-testing/blob/main/bag_logo.png?raw=true',
                'https://github.com/b-teh/map-testing/blob/main/IMG-20241112-WA0011.jpg?raw=true',
                'https://github.com/b-teh/map-testing/blob/main/LTL%20MICROPHONE.PNG?raw=true'
            ]

            image_names = ['Image ' + str(i) for i in range(len(image_urls))]
            n = len(image_urls)
            n_cols = 3
            i = 0
            index = 0
            with st.expander('Larger than Life'):
                cols = st.columns(n_cols)
                for im in image_urls:
                    with cols[i]:
                        with st.container(border = True):
                            # url = f"https://drive.google.com/uc?export=view&id={im}"
                            # response = requests.get(url) #google pull
                            st.image(im,width=200)
                            # st.text_input('Input something', key = str(index))
                            st.checkbox("select", key=index)
                    i = (i + 1) % n_cols
                    index += 1
                comments = st.text_input("Input comments")
            # Initialize session state variables for the index
            ordinary_collection_urls =['https://github.com/b-teh/map-testing/blob/main/Samples/IMG_7305.JPG?raw=true',
                                       'https://github.com/b-teh/map-testing/blob/main/Samples/IMG_7312.JPG?raw=true',
                                       'https://github.com/b-teh/map-testing/blob/main/Samples/IMG_7315.JPG?raw=true',
                                       'https://github.com/b-teh/map-testing/blob/main/Samples/IMG_7317.JPG?raw=true',
                                       'https://github.com/b-teh/map-testing/blob/main/Samples/IMG_7318.JPG?raw=true',
                                       'https://github.com/b-teh/map-testing/blob/main/Samples/IMG_7319.JPG?raw=true',
                                       'https://github.com/b-teh/map-testing/blob/main/Samples/IMG_7320.JPG?raw=true',
                                       'https://github.com/b-teh/map-testing/blob/main/Samples/IMG_7323.JPG?raw=true',
                                       'https://github.com/b-teh/map-testing/blob/main/Samples/IMG_7326.JPG?raw=true',
                                       'https://github.com/b-teh/map-testing/blob/main/Samples/IMG_7328.JPG?raw=true',
                                       'https://github.com/b-teh/map-testing/blob/main/Samples/IMG_7330.JPG?raw=true']
            with st.expander('Ordinary Collection'):
                cols = st.columns(4)
                i=0
                for im in ordinary_collection_urls:
                    with cols[i]:
                        with st.container(border=True):
                            st.image(im, width=200)
                            st.checkbox("select", key=index)
                    i = (i + 1) % 4
                    index += 1


    #analysis tab
    if show_tabs[2]:
        with used_tabs[2]:
            a1,a2 = st.columns([1,1.2])
            data = pd.DataFrame(abs(np.random.randn(24, 3)), columns=['Youths', 'Middle Aged', 'Seniors'])
            height = 450
            with a1:
                # with stylable_container(
                #         key="container_with_border",
                #         css_styles="""
                #             {"""+f"""
                #                border-radius: 20px;
                #                 border: 1px solid #ddd;
                #                 height: {height}px
                #                 padding: 10px;
                #                 resize: both;
                #                 overflow: auto;
                #            """+"""}
                #            """,
                # ):
                with st.container(border = True, height = height):
                    st.subheader("Hourly Foot Traffic")
                    # plot_bar()
                    st.bar_chart(data)
            with a2:
                # with stylable_container(
                #         key="container_with_border",
                #         css_styles="""
                #             {"""+f"""
                #                border-radius: 20px;
                #                 border: 1px solid #ddd;
                #                 height: {height}px
                #                 padding: calc(1em + 10000px);
                #                 resize: both;
                #                 overflow: auto;
                #            """+"""}
                #            """,
                # ):
                with st.container(border = True,height=height):
                    st.subheader("Project Outreach")
                    budget = st.slider("Select a budget value", min_value=0, max_value=100, value=50)
                    text1 = "Calculating Outreach"
                    text2 = "Sourcing Productions"
                    bar1 = st.progress(0, text=text1)
                    bar2 = st.progress(0, text=text2)
                    prog_rate = np.random.uniform(0.01, 0.03)
                    k = np.random.uniform(1.5, 2)
                    for i in range(101):
                        bar1.progress(min(int(k * i), 100), text=text1)
                        bar2.progress(i, text=text2)
                        time.sleep(prog_rate)

                    bar1.empty()
                    bar2.empty()

                    st.header("Project Details Dashboard")

                    def calc_metrics(budg):
                        manhours = round(budg * 50.718)
                        productions = max(int(budg / 25), 1)
                        pax = round(budg * 11.245)
                        return [str(pax), str(productions) , str(manhours) ]

                    metrics = calc_metrics(budget)
                    metric_names = ['Outreach (Pax)', 'Exhibits (Productions)', 'Engagement (mins)']
                    c = st.columns(len(metrics))
                    for i in range(len(metrics)):
                        c[i].metric(label=metric_names[i], value=metrics[i])
                    style_metric_cards(background_color="#FA8072", border_left_color="#F83C28")


st.set_page_config(page_title="MadCowMap",
                    page_icon='https://github.com/b-teh/map-testing/blob/main/MadCow.png?raw=true', layout='wide')
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


if st.session_state.logged_in:
    main_page()
else:
    login_page()
    if st.session_state.logged_in:
        main_page()



