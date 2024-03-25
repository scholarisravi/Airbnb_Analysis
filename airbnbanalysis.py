import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("Menu", ["Home","Explore data","Contact"],
                        icons=["house", "bar-chart-line","envelope"],
                        menu_icon="menu-button-wide",
                        default_index=0,
                        styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin": "-2px",
                                                "---hover-color": "#212223"},
                                "nav-link-selected": {"background-color": "#0C86C8"}})
    
                                                    
df = pd.read_csv(r"C:\Users\Ravishankar\Downloads\Airbnb_Analysis-main (1)\airbnbdata_Cleaned.csv",encoding='ISO-8859-1')

if selected == 'Home':
    st.markdown(
    """
    <style>
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0; }
        100% { opacity: 1; }
    }

    .blinking_text {
        animation: blink 1s infinite;
    }
    </style>
    """,
    unsafe_allow_html=True)
    
    st.markdown(
    """
    <style>
    .scrolling_text {
        animation: marquee 15s linear infinite;
    }

    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    </style>
    """,
    unsafe_allow_html=True)

    st.markdown(
    "<h1><span style='font-family:Papyrus; color:orange;'>📈<span class='blinking_text'>Airbnb Analysis</span></span></h1>", 
    unsafe_allow_html=True)  

    st.markdown(
    "<h4 style='font-family:Papyrus; color:rainbow;'>Technologies used: <marquee>Python Scripting, Mongodb, Data Preprocessing, Visualization, EDA, Streamlit, MongoDb, PowerBI or Tableau.</marquee></h4>",
    unsafe_allow_html=True)
    st.markdown("#### <span style='font-family:Papyrus; color:rainbow'>Industry Domain: Travel, Property Management, and Tourism.</span>", unsafe_allow_html=True)
    st.write("")
    st.markdown("#### <span style='font-family:Papyrus'>Airbnb, headquartered in San Francisco, is an American company that operates an online platform facilitating short- and long-term accommodation rentals and travel experiences. Acting as an intermediary, Airbnb charges a commission for each booking made through its platform. Established in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia, the company's name is a shortened form of its original title, AirBedandBreakfast.com. Airbnb is widely recognized for its transformative impact on the tourism sector, although it has also faced significant criticism from residents in popular tourist destinations such as Barcelona and Venice. Criticisms often revolve around concerns about escalating housing costs and a perceived lack of regulatory oversight.</span>", unsafe_allow_html=True)

# OVERVIEW PAGE
if selected == "Explore data":
    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country',sorted(df.country.unique()),sorted(df.country.unique()))
    prop = st.sidebar.multiselect('Select Property_type',sorted(df.property_type.unique()),sorted(df.property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(df.room_type.unique()),sorted(df.room_type.unique()))
    price = st.sidebar.slider('Select Price',df.price.min(),df.price.max(),(df.price.min(),df.price.max()))
    
    # CONVERTING THE USER INPUT INTO QUERY
    query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'
    
    # CREATING COLUMNS
    col1,col2 = st.columns(2,gap='large')
    
    with col1:
        st.markdown("### <span style='font-family:Papyrus;'>Average Price for Room Type</span>", unsafe_allow_html=True)
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.query(query).groupby('room_type',as_index=False)['price'].mean().sort_values(by='price')
        fig = px.bar(data_frame=pr_df,
                     x='room_type',
                     y='price',
                     color='price',
                    )
        st.plotly_chart(fig,use_container_width=True)

        st.markdown("### <span style='font-family:Papyrus;'>Availability Analysis</span>", unsafe_allow_html=True)
        fig = px.box(data_frame=df.query(query),
                     x='room_type',
                     y='availability_365',
                     color='room_type',
                    )
        st.plotly_chart(fig,use_container_width=True)

        st.markdown("### <span style='font-family:Papyrus;'>Host response based on country</span>", unsafe_allow_html=True)
        fig = px.scatter(df.query(query),
                    x='host_name',
                    y='host_response_time',
                    color='country_code', 
                    hover_name='name')
        fig.update_geos(projection_type='orthographic')
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        st.markdown("### <span style='font-family:Papyrus;'>Average Price in Country</span>", unsafe_allow_html=True)
        country_df = df.query(query).groupby('country',as_index=False)['price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='country',
                                       color= 'price', 
                                       hover_data=['price'],
                                       locationmode='country names',
                                       size='price',
                                       color_continuous_scale='agsunset'
                            )
        col2.plotly_chart(fig,use_container_width=True)
        
        st.markdown("### <span style='font-family:Papyrus;'>Availability in Country wise</span>", unsafe_allow_html=True)
        country_df = df.query(query).groupby('country',as_index=False)['availability_365'].mean()
        country_df.availability_365 = country_df.availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='country',
                                       color= 'availability_365', 
                                       hover_data=['availability_365'],
                                       locationmode='country names',
                                       size='availability_365',
                                       color_continuous_scale='agsunset'
                            )
        st.plotly_chart(fig,use_container_width=True)

        st.markdown("### <span style='font-family:Papyrus;'>Ratings based on country and price</span>", unsafe_allow_html=True)
        fig = px.scatter(df.query(query),
                    x='country',
                    y='price',
                    color='average_rating', 
                    hover_name='name')
        fig.update_geos(projection_type='orthographic')
        st.plotly_chart(fig,use_container_width=True)


    st.markdown("### <span style='font-family:Papyrus;'>Host response based on Country</span>", unsafe_allow_html=True)
    fig = px.scatter(df.query(query),
                x='host_name',
                y='host_response_time',
                color='country', 
                hover_name='name')
    fig.update_geos(projection_type='orthographic')
    st.plotly_chart(fig,use_container_width=True)

    st.markdown("### <span style='font-family:Papyrus;'>Beds and Bedrooms availability</span>", unsafe_allow_html=True)
    fig = px.pie(df.query(query), values='beds',
                         names='street',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['bedrooms'],
                         labels={'bedrooms': 'bedrooms'})

    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("### <span style='font-family:Papyrus;'>Beds and Bedrooms availability</span>", unsafe_allow_html=True)
    df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    st.map(df)
                

if selected == "Contact":
    st.markdown(
    "<h1><span style='font-family:Papyrus; color:orange;'>📈<span class='blinking_text'>Airbnb Analysis</span></span></h1>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<span style='font-family:Papyrus;'> This project focuses on analyzing Airbnb data leveraging MongoDB Atlas. It involves tasks such as data cleaning, preparation, and the creation of interactive geospatial visualizations. Dynamic plots are generated to explore pricing fluctuations, availability trends, and location-specific insights.</span>", unsafe_allow_html=True)            
    st.write("")
    st.write("**:orange[My GitHub link]** ⬇️")
    st.write("https://github.com/scholarisravi")
    st.write("**:orange[My Email]** ⬇️")
    st.write("Scholarisravi@gmail.com")

        