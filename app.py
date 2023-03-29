import streamlit as st
import pandas as pd
import preprocessor, helper

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df_2020 = pd.read_csv('2020_Olympics_Dataset.csv', encoding='unicode_escape')

df = preprocessor.preprocess(df, region_df)
df_2020 = preprocessor.preprocess_2020(df_2020, region_df)
df = preprocessor.merge(df, df_2020)

st.sidebar.header('Olympic Analysis')

user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Country-wise Analysis', 'Athelete-wise Analysis', 'Overall Analysis')
)

#st.dataframe(df_2020)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    year, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Year', year)
    selected_country = st.sidebar.selectbox('Country', country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Medal Analysis')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Overall tally of ' + str(selected_country))
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in year ' + str(selected_year))
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title('Medal Tally of '+ str(selected_country) + ' in '+ str(selected_year))

    st.table(medal_tally)