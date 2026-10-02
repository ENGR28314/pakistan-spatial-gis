import streamlit as st
import pandas as pd
import numpy as np
import json

st.set_page_config(
    page_title="Pakistan Spatial Master Layers GIS",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0d5c3a;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4a5568;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🇵🇰 Pakistan Spatial Master Layers GIS Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive Spatial Data Framework & Hydrological Link Canal Simulator</div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🗺️ GIS Master Layers")
layer_choice = st.sidebar.radio(
    "Select Domain to Explore:",
    [
        "1. Administrative Domains & Boundaries",
        "2. Mountain Walls & Forest Ecosystems",
        "3. Hydrology & Indus Water Treaty Simulator",
        "4. Lakes, Deserts, Oases & Islands",
        "5. Multi-Hazard Climatic & Tectonic Grids",
        "6. Raw GeoJSON Schema Exporter"
    ]
)

# -------------------------------------------------------------
# LAYER 1: ADMINISTRATIVE
# -------------------------------------------------------------
if "1." in layer_choice:
    st.header("📂 Spatial Boundaries & Administrative Domains")
    st.write("Complete hierarchy covering Provincial, Regional, and Maritime Zones (200 NM EEZ).")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Provinces & Regions", "7 Units")
    col2.metric("EEZ Maritime Area", "~240,000 km²")
    col3.metric("Land Boundary Length", "6,975 km")
    col4.metric("Coastline Length", "1,046 km")

    df_admin = pd.DataFrame({
        "Region / Territory": ["Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan", "Gilgit-Baltistan", "Azad Jammu & Kashmir", "Islamabad (ICT)"],
        "Capital": ["Lahore", "Karachi", "Peshawar", "Quetta", "Gilgit", "Muzaffarabad", "Islamabad"],
        "Area (km²)": [205344, 140914, 101741, 347190, 72971, 13297, 906],
        "Divisions": [10, 7, 7, 8, 3, 3, 1],
        "Districts": [42, 30, 36, 36, 14, 10, 1]
    })
    
    st.subheader("Administrative Metadata Table")
    st.dataframe(df_admin, use_container_width=True)

# -------------------------------------------------------------
# LAYER 2: TOPOGRAPHY & ECOSYSTEMS
# -------------------------------------------------------------
elif "2." in layer_choice:
    st.header("📂 Mountain Walls & Forest Ecosystems")
    st.write("Orographic convergence nodes of Northern Ranges and Western Fold Belts.")

    st.subheader("Major Mountain Ranges & High Peaks")
    df_mountains = pd.DataFrame({
        "Mountain Range": ["Karakoram", "Karakoram", "Himalayas", "Hindu Kush", "Sulaiman Range", "Kirthar Range"],
        "Peak Name": ["K2 (Godwin-Austen)", "Broad Peak", "Nanga Parbat", "Tirich Mir", "Takht-i-Sulaiman", "Zardak Peak"],
        "Elevation (meters)": [8611, 8051, 8125, 7708, 3487, 2260],
        "Region": ["Gilgit-Baltistan", "Gilgit-Baltistan", "Gilgit-Baltistan / AJK", "Khyber Pakhtunkhwa", "Balochistan / KP", "Sindh / Balochistan"]
    })
    st.dataframe(df_mountains, use_container_width=True)

    st.subheader("Key Ecological Biomes")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🌲 Ziarat Juniper Forest (Balochistan)**")
        st.caption("One of the world's oldest Juniperus excelsa habitats (over 2,500 years old), covering over 110,000 hectares.")
    with c2:
        st.markdown("**🌊 Coastal Riverine Mangroves (Indus Delta)**")
        st.caption("5th largest mangrove forest ecosystem in the world, dominated by Avicennia marina species.")

# -------------------------------------------------------------
# LAYER 3: HYDROLOGY & IWT SIMULATOR
# -------------------------------------------------------------
elif "3." in layer_choice:
    st.header("📂 Hydrological Axes & Indus Water Treaty Simulator")
    st.write("Simulate water routing from Western Rivers to Eastern River beds via the 7 Link Canals.")

    st.sidebar.subheader("🎛️ Reservoir Inflow Controls")
    tarbela_inflow = st.sidebar.slider("Tarbela Inflow (Indus) - MAF", 20, 100, 60)
    mangla_inflow = st.sidebar.slider("Mangla Inflow (Jhelum) - MAF", 5, 40, 20)
    
    st.sidebar.subheader("🔀 Link Canal Capacities (cusecs)")
    cj_cap = st.sidebar.slider("Chashma-Jhelum Link", 5000, 25000, 12000)
    tp_cap = st.sidebar.slider("Taunsa-Panjnad Link", 5000, 20000, 12000)
    rq_cap = st.sidebar.slider("Rasul-Qadirabad Link", 5000, 25000, 19000)
    qb_cap = st.sidebar.slider("Qadirabad-Balloki Link", 5000, 25000, 18600)
    bs_cap = st.sidebar.slider("Balloki-Sulemanki Link", 5000, 22000, 18500)

    total_inflow = tarbela_inflow + mangla_inflow
    est_sukkur_flow = round(total_inflow * 0.58, 2)
    est_kotri_flow = round(total_inflow * 0.35, 2)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total System Inflow", f"{total_inflow} MAF")
    col2.metric("Est. Sukkur Discharge", f"{est_sukkur_flow} MAF")
    col3.metric("Est. Kotri Outflow (Delta)", f"{est_kotri_flow} MAF")
    col4.metric("Active Link Canals", "7 System Canals")

    st.subheader("The 7 Indus Water Treaty Link Canals")
    df_canals = pd.DataFrame({
        "Link Canal Name": ["Chashma - Jhelum", "Taunsa - Panjnad", "Rasul - Qadirabad", "Qadirabad - Balloki", "Balloki - Sulemanki", "Marala - Ravi", "Bambanwala - Ravi - Bedian (BRB)"],
        "Source River": ["Indus", "Indus", "Jhelum", "Chenab", "Ravi", "Chenab", "Chenab"],
        "Destination River": ["Jhelum", "Chenab / Panjnad", "Chenab", "Ravi", "Sutlej", "Ravi", "Ravi / Sutlej"],
        "Current Capacity Setting (cusecs)": [cj_cap, tp_cap, rq_cap, qb_cap, bs_cap, 22000, 5000]
    })
    st.table(df_canals)

# -------------------------------------------------------------
# LAYER 4: LAKES, DESERTS & ISLANDS
# -------------------------------------------------------------
elif "4." in layer_choice:
    st.header("📂 Lakes, Deserts, Oases & Offshore Islands")
    
    tab1, tab2, tab3 = st.tabs(["🏞️ Major Lakes", "🏜️ Hyper-Arid Deserts", "🏝️ Offshore Islands"])
    
    with tab1:
        df_lakes = pd.DataFrame({
            "Lake Name": ["Manchar Lake", "Keenjhar Lake", "Attabad Lake", "Lake Saif-ul-Muluk"],
            "Type": ["Natural Freshwater / Wetland", "Freshwater Reservoir", "Landslide Dammed Lake", "High-Altitude Glacial"],
            "Location": ["Jamshoro / Dadu, Sindh", "Thatta, Sindh", "Hunza Valley, GB", "Kaghan Valley, KP"],
            "Key Role": ["Largest natural freshwater lake", "Primary drinking supply for Karachi", "Formed in 2010 landslide event", "High altitude ecotourism hub"]
        })
        st.dataframe(df_lakes, use_container_width=True)
        
    with tab2:
        df_deserts = pd.DataFrame({
            "Desert Name": ["Thar Desert", "Cholistan Desert", "Thal Desert", "Kharan Desert"],
            "Province": ["Sindh", "Punjab", "Punjab", "Balochistan"],
            "Climate Score": ["Hyper-Arid", "Hyper-Arid", "Arid / Semi-Arid", "Hyper-Arid Hyper-Thermal"],
            "Associated Oases": ["Umerkot Oasis", "Derawar Belt", "Indus Oasis Fringe", "Mastung & Panjgur Oases"]
        })
        st.dataframe(df_deserts, use_container_width=True)

    with tab3:
        st.markdown("**🏝️ Astola Island (Jezira Haft Talar)** - Located off the Pasni coast, Balochistan. First Marine Protected Area (MPA) in Pakistan.")
        st.markdown("**🏝️ Churna Island** - Located off Hub/Karachi coast. Key coral reef and marine biodiversity hub.")

# -------------------------------------------------------------
# LAYER 5: MULTI-HAZARD & SEISMIC
# -------------------------------------------------------------
elif "5." in layer_choice:
    st.header("📂 Multi-Hazard Climatic & Geological Grids")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("⚡ Tectonic Fault Lines")
        st.error("**Chaman Fault Line:** Strike-slip active transform fault extending ~860 km through Balochistan into Afghanistan.")
        st.warning("**Main Boundary Thrust (MBT):** Active Himalayan thrust zone running through AJK, KP, and Northern Punjab.")

    with c2:
        st.subheader("🌊 Hydrometeorological Hazard Belts")
        st.info("**GLOF Hazard Basins:** Over 3,044 glacial lakes mapped in GB & KP, with 33 identified at high risk of outburst.")
        st.warning("**Monsoon Flood Plains:** Riverine and flash flood inundation vectors along the Indus River corridor.")

# -------------------------------------------------------------
# LAYER 6: GEOJSON EXPORTER
# -------------------------------------------------------------
elif "6." in layer_choice:
    st.header("📂 Master Spatial Data Schema (GeoJSON Exporter)")
    st.write("Export the complete GIS layer schema definition for integration into QGIS, ArcGIS, or Leaflet.")

    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Tarbela Dam Node", "category": "Hydrology", "type": "Mega Reservoir", "capacity_MAF": 11.6},
                "geometry": {"type": "Point", "coordinates": [72.6983, 34.0883]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Mangla Dam Node", "category": "Hydrology", "type": "Reservoir", "capacity_MAF": 7.39},
                "geometry": {"type": "Point", "coordinates": [73.6425, 33.1461]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Astola Island", "category": "Islands", "type": "Marine Protected Area"},
                "geometry": {"type": "Point", "coordinates": [63.8542, 25.1225]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Chaman Fault Line Segment", "category": "Hazard", "type": "Transform Fault"},
                "geometry": {"type": "LineString", "coordinates": [[66.5, 30.2], [66.6, 30.9], [66.8, 31.5]]}
            }
        ]
    }

    st.json(geojson_data)
    st.download_button(
        label="📥 Download Master GeoJSON Schema",
        data=json.dumps(geojson_data, indent=2),
        file_name="pakistan_spatial_master_layers.geojson",
        mime="application/json"
    )
