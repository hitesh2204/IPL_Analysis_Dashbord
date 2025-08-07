import pandas as pd

def generate_bowling_phase_stats(df):
    phase_ranges = {
        "Powerplay": (1, 6),
        "Middle Overs": (7, 15),
        "Death Overs": (16, 20)
    }

    records = []

    for bowler in df["bowler"].unique():
        bowler_df = df[df["bowler"] == bowler]

        for phase, (start_over, end_over) in phase_ranges.items():
            phase_df = bowler_df[(bowler_df["overs"] >= start_over) & (bowler_df["overs"] <= end_over)]
            if phase_df.empty:
                continue

            balls = phase_df.shape[0]
            runs_conceded = phase_df["total_run"].sum()
            wickets = phase_df[phase_df["isWicketDelivery"] == 1]["player_out"].notnull().sum()
            overs_bowled = balls / 6
            economy = runs_conceded / overs_bowled if overs_bowled else 0
            bowling_avg = runs_conceded / wickets if wickets else 0
            strike_rate = balls / wickets if wickets else 0

            records.append({
                "bowler": bowler,
                "phase": phase,
                "balls": balls,
                "overs_bowled": round(overs_bowled, 2),
                "runs_conceded": runs_conceded,
                "wickets": wickets,
                "economy_rate": round(economy, 2),
                "average": round(bowling_avg, 2) if wickets else None,
                "strike_rate": round(strike_rate, 2) if wickets else None
            })

    return pd.DataFrame(records)

if __name__ == "__main__":
    df = pd.read_csv("IPL_Dataset/final_ipl.csv", encoding="ISO-8859-1")
    bowling_phase_df = generate_bowling_phase_stats(df)
    bowling_phase_df.to_csv("IPL_Dataset/rag_knowledgebase/bowling_phase_stats.csv", index=False)
