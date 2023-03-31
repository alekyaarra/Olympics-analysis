import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df_2020 = pd.read_csv('2020_Olympics_Dataset.csv', encoding='unicode_escape')

df = preprocessor.preprocess(df, region_df)
df_2020 = preprocessor.preprocess_2020(df_2020, region_df)
df = preprocessor.merge(df, df_2020)

st.sidebar.header('Olympic Analysis')

user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis', 'Country-wise Analysis', 'Athelete-wise Analysis')
)

#st.dataframe(df_2020)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    year, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Year', year)
    selected_country = st.sidebar.selectbox('Country', country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Total Medal Analysis')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Medal tally of ' + str(selected_country))
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in year ' + str(selected_year))
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title('Medal Tally of '+ str(selected_country) + ' in '+ str(selected_year))

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] -1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    participants = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Statistics')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(participants)
    with col3:
        st.header('Nations')
        st.title(nations)

    nations_over_time=helper.nations_over_time(df)
    fig = px.line(nations_over_time, x="Edition", y="No of Nations")
    st.title("Nations participating over the years")
    st.plotly_chart(fig)

    events_over_time = helper.events_over_time(df)
    fig = px.line(events_over_time, x="Edition", y="No of Events")
    st.title("No of Events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.athletes_over_time(df)
    fig = px.line(athletes_over_time, x="Edition", y="No of Athletes")
    st.title("No of Athletes over the years")
    st.plotly_chart(fig)