import numpy as np

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list (df):
    year = df['Year'].unique().tolist()
    year.sort(reverse = True)
    year.insert(0, 'Overall')

    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return year, countries


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                    ascending=False).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def nations_over_time(df, sport):
    temp_df=df
    if sport != 'Overall':
        temp_df = df[df['Sport'] == sport]

    nations_over_time = temp_df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('index',
                                                                                                                ascending=False)
    nations_over_time.rename(columns={"index": "Edition", "Year": "No of Nations"}, inplace=True)
    return(nations_over_time)

def events_over_time(df, sport):
    temp_df = df
    if sport != 'Overall':
        temp_df = df[df['Sport'] == sport]

    events_over_time=temp_df.drop_duplicates(['Year','Event'])['Year'].value_counts().reset_index().sort_values('index', ascending=False)
    events_over_time.rename(columns={"index": "Edition", "Year": "No of Events"}, inplace=True)
    return(events_over_time)

def athletes_over_time(df, sport):
    temp_df = df
    if sport != 'Overall':
        temp_df = df[df['Sport'] == sport]

    athletes_over_time=temp_df.drop_duplicates(['Year','Name'])['Year'].value_counts().reset_index().sort_values('index', ascending=False)
    athletes_over_time.rename(columns={"index": "Edition", "Year": "No of Athletes"}, inplace=True)
    return(athletes_over_time)

def most_successful(df, sport):
  temp_df = df.dropna(subset=['Medal'])
  if sport != 'Overall':
    temp_df = temp_df[temp_df['Sport'] == sport]
  x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name', how='left')[['index','Name_x','Sport','NOC']].drop_duplicates(['index'])
  x.rename(columns={'index':'Name','Name_x':'Medal count'}, inplace=True)
  # x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
  #     ['index']].drop_duplicates(['index'])
  # x.rename(columns={'index': 'Name'}, inplace=True)
  return x

