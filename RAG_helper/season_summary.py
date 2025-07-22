import pandas as pd

def clean_season_column(df):
    def extract_year(season):
        if isinstance(season, str) and '/' in season:
            parts = season.split('/')
            if len(parts) == 2:
                return int("20" + parts[1])
        try:
            return int(season)
        except:
            return None

    df['Season'] = df['Season'].apply(extract_year)
    df = df.dropna(subset=['Season'])
    df['Season'] = df['Season'].astype(int)
    return df

def generate_season_summary_csv(ipl):
    ipl = clean_season_column(ipl)

    summary_list = []

    for season in sorted(ipl['Season'].unique()):
        season_df = ipl[ipl['Season'] == season]

        total_matches = season_df['ID'].nunique()
        total_runs = season_df['batsman_run'].sum()

        # Top Scorer
        top_batsman_df = season_df.groupby('batter')['batsman_run'].sum().reset_index()
        top_batsman_df = top_batsman_df.sort_values(by='batsman_run', ascending=False)
        top_scorer = top_batsman_df.iloc[0]['batter']
        top_scorer_runs = int(top_batsman_df.iloc[0]['batsman_run'])

        # Top Wicket Taker
        wicket_df = season_df[season_df['player_out'].notnull()]
        top_bowler_df = wicket_df.groupby('bowler')['player_out'].count().reset_index()
        top_bowler_df = top_bowler_df.sort_values(by='player_out', ascending=False)
        top_wicket_taker = top_bowler_df.iloc[0]['bowler']
        top_wickets = int(top_bowler_df.iloc[0]['player_out'])

        summary_list.append({
            'season': season,
            'total_matches': total_matches,
            'total_runs': total_runs,
            'top_scorer': top_scorer,
            'top_scorer_runs': top_scorer_runs,
            'top_wicket_taker': top_wicket_taker,
            'top_wickets': top_wickets
        })

    season_summary_df = pd.DataFrame(summary_list)
    season_summary_df.to_csv("ipl_dataset//rag_knowledgebase//season_summary.csv", index=False)
    print("✅ Clean season_summary.csv generated (without winner)!")

if __name__ == "__main__":
    ipl_df = pd.read_csv("ipl_dataset//ipl_df.csv")
    generate_season_summary_csv(ipl_df)
