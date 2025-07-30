import pandas as pd

def calculate_player_vs_team(csv_path):
    df = pd.read_csv(csv_path,encoding='ISO-8859-1')
    df = df.dropna(subset=["batter", "bowler"])

    # Combine batting and bowling players
    players = set(df["batter"].unique()).union(set(df["bowler"].unique()))
    teams = df["BattingTeam"].unique()

    data = []

    for player in players:
        for team in teams:
            # Batting vs team
            bdf = df[(df["batter"] == player) & (df["BowlingTeam"] == team)]
            matches_batted = bdf["ID"].nunique()
            total_runs = bdf["batsman_run"].sum()
            balls_faced = bdf["ballnumber"].count()
            fours = (bdf["batsman_run"] == 4).sum()
            sixes = (bdf["batsman_run"] == 6).sum()

            match_runs = bdf.groupby("ID")["batsman_run"].sum()
            fifties = match_runs[(match_runs >= 50) & (match_runs < 100)].count()
            hundreds = match_runs[match_runs >= 100].count()

            dismissals = df[(df["player_out"] == player) & (df["BowlingTeam"] == team)].shape[0]
            strike_rate = (total_runs / balls_faced) * 100 if balls_faced else 0
            batting_avg = (total_runs / dismissals) if dismissals else None

            # Bowling vs team
            bwdf = df[(df["bowler"] == player) & (df["BattingTeam"] == team)]
            balls_bowled = bwdf["ballnumber"].count()
            runs_conceded = bwdf["total_run"].sum()
            wickets = bwdf["player_out"].notna().sum()
            overs = balls_bowled // 6 + (balls_bowled % 6) / 10
            economy = runs_conceded / overs if overs else 0
            bowling_avg = runs_conceded / wickets if wickets else None

            wickets_by_match = bwdf[bwdf["player_out"].notna()].groupby("ID")["player_out"].count()
            five_wkts = wickets_by_match[wickets_by_match >= 5].count()

            data.append({
                "Player": player,
                "AgainstTeam": team,
                "MatchesBatted": matches_batted,
                "Runs": total_runs,
                "BallsFaced": balls_faced,
                "Fours": fours,
                "Sixes": sixes,
                "50s": fifties,
                "100s": hundreds,
                "Dismissals": dismissals,
                "StrikeRate": round(strike_rate, 2) if balls_faced else 0,
                "BattingAverage": round(batting_avg, 2) if batting_avg else None,
                "BallsBowled": balls_bowled,
                "RunsConceded": runs_conceded,
                "Wickets": wickets,
                "5w": five_wkts,
                "Overs": round(overs, 2) if overs else 0,
                "Economy": round(economy, 2) if economy else None,
                "BowlingAverage": round(bowling_avg, 2) if bowling_avg else None,
            })

    result_df = pd.DataFrame(data)
    result_df.to_csv("IPL_Dataset//rag_knowledgebase//player_vs_team_stats.csv", index=False)
    print("✅ Saved 'player_vs_team_stats.csv' with player vs opponent team performance.")

# Example usage:
# calculate_player_vs_team("final_ipl.csv")
if __name__=="__main__":
    calculate_player_vs_team("IPL_Dataset//final_ipl.csv")