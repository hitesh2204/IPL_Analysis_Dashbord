import pandas as pd

def calculate_player_stats(csv_path):
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')
    df = df.dropna(subset=["batter", "bowler"])

    player_stats = {}

    batters = df.groupby("batter")
    bowlers = df.groupby("bowler")

    all_players = set(df["batter"].unique()).union(set(df["bowler"].unique()))

    for player in all_players:
        # Batting stats
        if player in batters.groups:
            bdf = batters.get_group(player)
            total_runs = bdf["batsman_run"].sum()
            balls_faced = bdf["ballnumber"].count()
            fours = (bdf["batsman_run"] == 4).sum()
            sixes = (bdf["batsman_run"] == 6).sum()
            matches = bdf["ID"].nunique()
            innings = bdf["ID"].nunique()

            player_match_runs = bdf.groupby("ID")["batsman_run"].sum()
            fifties = player_match_runs[(player_match_runs >= 50) & (player_match_runs < 100)].count()
            hundreds = player_match_runs[player_match_runs >= 100].count()

            dismissals = df[(df["player_out"] == player)].shape[0]
            strike_rate = (total_runs / balls_faced) * 100 if balls_faced else 0
            batting_avg = (total_runs / dismissals) if dismissals else None
        else:
            total_runs = balls_faced = fours = sixes = matches = innings = strike_rate = batting_avg = dismissals = fifties = hundreds = 0

        # Bowling stats
        if player in bowlers.groups:
            bwdf = bowlers.get_group(player)
            balls_bowled = bwdf["ballnumber"].count()
            runs_conceded = bwdf["total_run"].sum()
            wickets = bwdf["player_out"].notna().sum()
            overs = balls_bowled // 6 + (balls_bowled % 6) / 10
            economy = runs_conceded / overs if overs else 0
            bowling_avg = runs_conceded / wickets if wickets else None

            # 5-wicket hauls
            wickets_by_match = bwdf[bwdf["player_out"].notna()].groupby("ID")["player_out"].count()
            five_wkts = wickets_by_match[wickets_by_match >= 5].count()
        else:
            balls_bowled = runs_conceded = wickets = overs = economy = bowling_avg = five_wkts = 0

        player_stats[player] = {
            "Matches": matches,
            "Innings": innings,
            "Runs": total_runs,
            "BallsFaced": balls_faced,
            "Fours": fours,
            "Sixes": sixes,
            "Dismissals": dismissals,
            "50s": fifties,
            "100s": hundreds,
            "StrikeRate": round(strike_rate, 2) if strike_rate else 0,
            "BattingAverage": round(batting_avg, 2) if batting_avg else None,
            "BallsBowled": balls_bowled,
            "RunsConceded": runs_conceded,
            "Wickets": wickets,
            "5w": five_wkts,
            "Overs": round(overs, 2) if overs else 0,
            "Economy": round(economy, 2) if economy else None,
            "BowlingAverage": round(bowling_avg, 2) if bowling_avg else None
        }

    final_df = pd.DataFrame.from_dict(player_stats, orient='index').reset_index().rename(columns={"index": "Player"})
    final_df.to_csv("IPL_Dataset//rag_knowledgebase//player_stats.csv", index=False)
    print("✅ Player stats saved to 'player_stats.csv'")

# Example usage:
# calculate_player_stats("final_ipl.csv")
if __name__=="__main__":
    calculate_player_stats("IPL_Dataset//final_ipl.csv")