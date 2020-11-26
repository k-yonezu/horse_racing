import as pd

df = rd.read_horse_csv(DATA_PATH)
def create_horse_data(n_race, df):
    df.sort_values("date", inplace=True)
    race_df = df.iloc[-1:, :].reset_index(drop=True)
    columns = race_df.columns
    for n in range(1, n_race+1):
        add_columns = list(map(lambda c: c+f"_{n}", columns))
        add_race = df.iloc[-1-n:-n, :].reset_index(drop=True)
        add_race.columns = add_columns
        race_df = pd.concat([race_df, add_race], axis=1)
    return race_df

