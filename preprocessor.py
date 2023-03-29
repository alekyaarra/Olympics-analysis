import pandas as pd

def preprocess(df, region_df):
    df = df[df['Season'] == 'Summer']
    df = df.merge(region_df, on='NOC', how='left')
    df = df.drop(['Height', 'Weight'], axis=1)
    df.drop_duplicates(inplace=True)

    return df

def preprocess_2020(df_2020, region_df):
    df_2020 = df_2020.drop(['Discipline', 'Rank'], axis=1)
    df_2020['Season'] = 'Summer'
    df_2020 = df_2020.merge(region_df, on='NOC', how='left')
    df_2020['Games'] = '2020 Summer'
    df_2020['Year'] = 2020
    df_2020['city'] = 'Tokyo'
    df_2020 = df_2020.assign(ID=range(1, len(df_2020) + 1))
    df_2020 = df_2020.drop(['Unnamed: 0', 'Code'], axis=1)
    df_2020.rename(columns={'Gender': 'Sex', 'Country': 'Team'}, inplace=True)
    df_2020.loc[df_2020["Sex"] == "Male", "Sex"] = 'M'
    df_2020.loc[df_2020["Sex"] == "Female", "Sex"] = 'F'
    new_cols = ["ID","Name","Sex","Age",'Team','NOC','Games','Year','Season','city','Sport','Event','Medal','region','notes']
    df_2020 = df_2020.reindex(columns=new_cols)
    df_2020.rename(columns={'city': 'City'}, inplace=True)

    return df_2020

def merge(df,df_2020):
    df = df.append(df_2020, ignore_index=True)
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df