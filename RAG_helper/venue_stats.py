import pandas as pd
from src.data_loader import load_ipl_data

def generate_venue_stats_per_season(df):
    venue_stats = []

    # Group by season + venue
    for (season, venue), temp in df.groupby(["Season", "Venue"]):
        total_matches = temp["ID"].nunique()

        # first/second innings subsets for averages
        first_innings = temp[temp["innings"] == 1]
        second_innings = temp[temp["innings"] == 2]

        # Initialize counters
        bat1st_wins = 0
        chasing_wins = 0
        no_result = 0

        # iterate per match to determine batting order and winner
        for match_id, mdf in temp.groupby("ID"):
            # get unique batting teams in order of appearance
            teams = mdf["BattingTeam"].dropna().unique().tolist()

            # if only one team present (abandoned / incomplete innings), treat as no result
            if len(teams) < 2:
                no_result += 1
                continue

            team1 = teams[0]   # batted first
            team2 = teams[1]   # batted second (chasing)

            # find winning team for this match (if present)
            winners = mdf["WinningTeam"].dropna().unique().tolist()
            if not winners:
                # no winning team recorded -> no result / abandoned
                no_result += 1
                continue

            winning_team = winners[0]

            # categorize
            if winning_team == team1:
                bat1st_wins += 1
            elif winning_team == team2:
                chasing_wins += 1
            else:
                # a corner case: WinningTeam not equal to either batting team (data issue)
                no_result += 1

        bat1st_win_pct = round((bat1st_wins / total_matches) * 100, 2) if total_matches else 0.0
        chasing_win_pct = round((chasing_wins / total_matches) * 100, 2) if total_matches else 0.0

        # averages
        avg_1st_innings_score = first_innings.groupby("ID")["total_run"].sum().mean()
        avg_2nd_innings_score = second_innings.groupby("ID")["total_run"].sum().mean()

        total_scores = temp.groupby("ID")["total_run"].sum()
        highest_total = int(total_scores.max()) if not total_scores.empty else 0
        lowest_total = int(total_scores.min()) if not total_scores.empty else 0

        total_fours = int((temp["batsman_run"] == 4).sum())
        total_sixes = int((temp["batsman_run"] == 6).sum())
        total_runs = int(temp["total_run"].sum())

        # Player milestones (fifties/hundreds) per match at this venue & season
        player_scores = temp.groupby(["ID", "batter"])["batsman_run"].sum()
        total_hundreds = int((player_scores >= 100).sum())
        total_fifties = int(((player_scores >= 50) & (player_scores < 100)).sum())

        # Top 5 batsmen (runs at this venue+season)
        top_batsmen = (
            temp.groupby("batter")["batsman_run"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )

        # Top 5 bowlers (wickets)
        top_bowlers = (
            temp[temp["isWicketDelivery"] == 1]
            .groupby("bowler")
            .size()
            .sort_values(ascending=False)
            .head(5)
            .reset_index(name="wickets")
        )

        venue_stats.append({
            "Season": season,
            "Venue": venue,
            "total_matches": int(total_matches),
            "bat1st_wins": bat1st_wins,
            "chasing_wins": chasing_wins,
            "no_result": no_result,
            "bat1st_win_pct": bat1st_win_pct,
            "chasing_win_pct": chasing_win_pct,
            "avg_1st_innings_score": round(avg_1st_innings_score, 2) if not pd.isna(avg_1st_innings_score) else 0,
            "avg_2nd_innings_score": round(avg_2nd_innings_score, 2) if not pd.isna(avg_2nd_innings_score) else 0,
            "highest_total": highest_total,
            "lowest_total": lowest_total,
            "total_fours": total_fours,
            "total_sixes": total_sixes,
            "total_runs": total_runs,
            "total_hundreds": total_hundreds,
            "total_fifties": total_fifties,
            "top_5_batsmen": top_batsmen.to_dict("records"),
            "top_5_bowlers": top_bowlers.to_dict("records")
        })

    return pd.DataFrame(venue_stats)


if __name__ == "__main__":
    df = load_ipl_data()
    venue_df = generate_venue_stats_per_season(df)
    venue_df.to_csv("IPL_Dataset/rag_knowledgebase/venue_stats_season1.csv", index=False)
    print("✅ venue_stats_per_season.csv generated successfully")
