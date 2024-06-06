import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
from PIL import Image
import warnings
import os

warnings.filterwarnings('ignore')

st.set_page_config(page_title="AirBnb-Analysis", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart:   AirBnb-Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

SELECT = option_menu(
    menu_title=None,
    options=["Home", "Explore Data", "Contact"],
    icons=["house", "bar-chart", "at"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white", "size": "cover", "width": "100"},
            "icon": {"color": "black", "font-size": "20px"},
            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
            "nav-link-selected": {"background-color": "#6F36AD"}})

filename = None  # Initialize filename with a default value
df = None  # Initialize df with a default value

# ----------------Home----------------------#
if SELECT == "Home":
    st.header('Airbnb Analysis')
    st.subheader("...")  # Add your content here

# ----------------Explore Data----------------------#
if SELECT == "Explore Data":
    fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
    
    if fl is not None:
        try:
            filename = fl.name
            st.write(filename)
            df = pd.read_csv(fl, encoding="ISO-8859-1")
        except pd.errors.EmptyDataError:
            st.warning("The uploaded file is empty.")
    else:
        st.write("Please Choose A File Above For Visualization")

    st.sidebar.header("Choose your filter: ")

    if df is not None:
        neighbourhood_group = st.sidebar.multiselect("Pick your neighbourhood_group", df["neighbourhood_group"].unique())
        if not neighbourhood_group:
            df2 = df.copy()
        else:
            df2 = df[df["neighbourhood_group"].isin(neighbourhood_group)]

        neighbourhood = st.sidebar.multiselect("Pick the neighbourhood", df2["neighbourhood"].unique())
        if not neighbourhood:
            df3 = df2.copy()
        else:
            df3 = df2[df2["neighbourhood"].isin(neighbourhood)]

        filtered_df = df3

        if neighbourhood_group:
            filtered_df = filtered_df[filtered_df["neighbourhood_group"].isin(neighbourhood_group)]

        if neighbourhood:
            filtered_df = filtered_df[filtered_df["neighbourhood"].isin(neighbourhood)]

        room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("room_type_ViewData")
            fig = px.bar(room_type_df, x="room_type", y="price", text=['${:,.2f}'.format(x) for x in room_type_df["price"]],
                         template="seaborn")
            st.plotly_chart(fig, use_container_width=True, height=200)

        with col2:
            st.subheader("neighbourhood_group_ViewData")
            fig = px.pie(filtered_df, values="price", names="neighbourhood_group", hole=0.5)
            fig.update_traces(text=filtered_df["neighbourhood_group"], textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

        cl1, cl2 = st.columns((2))
        with cl1:
            with st.expander("room_type wise price"):
                st.write(room_type_df.style.background_gradient(cmap="Blues"))
                csv = room_type_df.to_csv(index=False).encode('utf-8')
                st.download_button("Download Data", data=csv, file_name="room_type.csv", mime="text/csv",
                                   help='Click here to download the data as a CSV file')

        with cl2:
            with st.expander("neighbourhood_group wise price"):
                neighbourhood_group = filtered_df.groupby(by="neighbourhood_group", as_index=False)["price"].sum()
                st.write(neighbourhood_group.style.background_gradient(cmap="Oranges"))
                csv = neighbourhood_group.to_csv(index=False).encode('utf-8')
                st.download_button("Download Data", data=csv, file_name="neighbourhood_group.csv", mime="text/csv",
                                   help='Click here to download the data as a CSV file')

        data1 = px.scatter(filtered_df, x="neighbourhood_group", y="neighbourhood", color="room_type")
        data1['layout'].update(title="Room_type in the Neighbourhood and Neighbourhood_Group wise data using Scatter Plot.",
                               titlefont=dict(size=20), xaxis=dict(title="Neighbourhood_Group", titlefont=dict(size=20)),
                               yaxis=dict(title="Neighbourhood", titlefont=dict(size=20)))
        st.plotly_chart(data1, use_container_width=True)

        with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
            st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

        import plotly.figure_factory as ff

        st.subheader(":point_right: Neighbourhood_group wise Room_type and Minimum stay nights")
        with st.expander("Summary_Table"):
            df_sample = df[0:5][["neighbourhood_group", "neighbourhood", "reviews_per_month", "room_type", "price",
                                  "minimum_nights", "host_name"]]
            fig = ff.create_table(df_sample, colorscale="Cividis")
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Airbnb Analysis in Map view")
        df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
        st.map(df)

col1, col2 = st.columns(2)

with col1:
    image1 = Image.open("/Users/mohitr/Downloads/Airbnb Logo PNG Transparent & SVG Vector - Freebie Supply.jpg")
    st.image(image1, width=300)

with col2:
    col2.subheader("NAME : mohit ")
    col2.subheader("EMAIL: mr8574190@gmail.com")
    col2.subheader("BATCH : D90D94D95")
