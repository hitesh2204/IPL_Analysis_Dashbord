import pandas as pd

def update_playoff_stats(df):
    playoff_matches = df[df["MatchNumber"].str.contains("Qualifier|Eliminator|Final", case=False, na=False)]
    records = []

    for player in playoff_matches["batter"].unique():
        player_df = playoff_matches[playoff_matches["batter"] == player]
        runs = player_df["batsman_run"].sum()
        balls = player_df.shape[0]
        strike_rate = (runs / balls) * 100 if balls else 0

        # Bowling side for same player
        bowling_df = playoff_matches[playoff_matches["bowler"] == player]
        wickets = bowling_df[bowling_df["isWicketDelivery"] == 1]["player_out"].notnull().sum()
        runs_conceded = bowling_df["total_run"].sum()
        overs_bowled = bowling_df.shape[0] / 6
        economy = runs_conceded / overs_bowled if overs_bowled else 0

        records.append({
            "player": player,
            "total_runs": runs,
            "balls_faced": balls,
            "strike_rate": round(strike_rate, 2),
            "wickets": wickets,
            "runs_conceded": runs_conceded,
            "economy": round(economy, 2) if overs_bowled else None
        })

    return pd.DataFrame(records)

if __name__ == "__main__":
    df = pd.read_csv("IPL_Dataset/final_ipl.csv", encoding="ISO-8859-1")
    playoff_stats_df = update_playoff_stats(df)
    playoff_stats_df.to_csv("IPL_Dataset/rag_knowledgebase/playoff_stats.csv", index=False)
