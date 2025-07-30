import pandas as pd

def generate_bowler_vs_team_stats(csv_path):
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')

    df = df.dropna(subset=["bowler", "BattingTeam"])
    df["is_wicket"] = df["player_out"].notna()

    # One row = one delivery ⇒ count rows per match
    per_match_stats = df.groupby(["bowler", "BattingTeam", "ID"]).agg({
        "total_run": "sum",
        "is_wicket": "sum"
    }).reset_index()

    # Add delivery count manually
    delivery_counts = df.groupby(["bowler", "BattingTeam", "ID"]).size().reset_index(name="deliveries")
    per_match_stats = per_match_stats.merge(delivery_counts, on=["bowler", "BattingTeam", "ID"])

    final_stats = []

    for (bowler, team), group in per_match_stats.groupby(["bowler", "BattingTeam"]):
        balls = group["deliveries"].sum()
        runs = group["total_run"].sum()
        wickets = group["is_wicket"].sum()
        matches = group.shape[0]

        overs = balls // 6 + (balls % 6) / 10
        economy = runs / (balls / 6) if balls else 0
        avg = runs / wickets if wickets else None
        strike_rate = balls / wickets if wickets else None

        # 3w and 5w hauls
        three_wkts = (group["is_wicket"] >= 3).sum()
        five_wkts = (group["is_wicket"] >= 5).sum()
        best_wkts = int(group["is_wicket"].max()) if not group["is_wicket"].isnull().all() else "-"

        final_stats.append({
            "Bowler": bowler,
            "AgainstTeam": team,
            "Matches": matches,
            "BallsBowled": balls,
            "Overs": round(overs, 2),
            "RunsConceded": runs,
            "Wickets": wickets,
            "3w": three_wkts,
            "5w": five_wkts,
            "BestFigure": best_wkts,
            "Economy": round(economy, 2),
            "Average": round(avg, 2) if avg else None,
            "StrikeRate": round(strike_rate, 2) if strike_rate else None,
        })

    df_result = pd.DataFrame(final_stats)
    df_result.to_csv("IPL_Dataset//rag_knowledgebase//bowler_vs_teams.csv", index=False)
    print("✅ Bowler vs Team stats saved successfully.")

if __name__ == "__main__":
    generate_bowler_vs_team_stats("IPL_Dataset//final_ipl.csv")
