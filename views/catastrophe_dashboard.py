import streamlit as st
import pandas as pd
import plotly.express as px

# LOAD DATA
df = pd.read_csv("Data\original_with_coordinates.csv")

# CONVER DATA TO COLUMN
df['Date'] = pd.to_datetime(df['Date'])

# SECTION TITLE
st.title("Global Disaster Dashboard")

# ----------------------------
# FILTER CONTROL
# ----------------------------
st.subheader("Filter Options")

locations = df['Location'].dropna().unique().tolist()
disaster_types = df['Disaster_Type'].dropna().unique().tolist()
min_date, max_date = df['Date'].min(), df['Date'].max()

col1, col2, col3 = st.columns(3)
with col1:
    selected_locs = st.multiselect("Location", locations, default=locations)
with col2:
    selected_types = st.multiselect("Disaster Type", disaster_types, default=disaster_types)
with col3:
    selected_dates = st.date_input("Date Range", [min_date, max_date])

# Filter the data
filtered = df[
    (df['Location'].isin(selected_locs)) &
    (df['Disaster_Type'].isin(selected_types)) &
    (df['Date'] >= pd.to_datetime(selected_dates[0])) &
    (df['Date'] <= pd.to_datetime(selected_dates[1]))
]

# ----------------------------
# MAP VIEW
# ----------------------------
st.subheader("Disaster Locations Map")

# Aggregate the count of disasters per location
location_counts = (
    filtered.groupby(['Latitude', 'Longitude', 'Location', 'Disaster_Type'])
    .size()
    .reset_index(name='Disaster_Count')
)

# Plot using size
fig_map = px.scatter_mapbox(
    location_counts,
    lat="Latitude",
    lon="Longitude",
    size="Disaster_Count",
    color="Disaster_Type",
    hover_name="Location",
    hover_data=["Disaster_Count"],
    zoom=1,
    height=450
)

fig_map.update_layout(
    mapbox_style="carto-darkmatter",  # or "white-bg", "darkmatter"
    margin={"r":0,"t":0,"l":0,"b":0}
)

fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_map)

# ----------------------------
# GRAPHS
# ----------------------------

with st.expander("See details"):
    col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
    with col1:
        # Histogram of Magnitudes
        fig1 = px.histogram(
            filtered,
            x='Magnitude',
            nbins=20,
            title='Distribution of Disaster Magnitudes',
            color_discrete_sequence=['#636EFA']
        )

        fig1.update_traces(marker_line_color="white", marker_line_width=1.2)
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"),
            bargap=0.2
        )
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        # Pie Chart by Disaster Type
        fig2 = px.pie(filtered, names='Disaster_Type', title='Proportion of Disaster Types')
        st.plotly_chart(fig2, use_container_width=True)

    # Bar chart of fatalities by location
    fatalities = filtered.groupby("Location")["Fatalities"].sum().reset_index()
    fig3 = px.histogram(
        fatalities,
        x="Location",
        y="Fatalities",
        title="Total Fatalities by Location",
        color_discrete_sequence=['#636EFA']
    )

    fig3.update_traces(marker_line_color="white", marker_line_width=1.2)
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        bargap=0.2
    )

    st.plotly_chart(fig3, use_container_width=True)