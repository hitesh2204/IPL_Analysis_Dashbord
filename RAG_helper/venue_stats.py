import pandas as pd

def generate_venue_stats(df):
    venue_stats = []

    venues = df["Venue"].unique()

    for venue in venues:
        temp = df[df["Venue"] == venue]

        total_matches = temp["ID"].nunique()
        first_innings = temp[temp["innings"] == 1]
        second_innings = temp[temp["innings"] == 2]

        match_outcome = temp.groupby("ID").agg({
            "innings": list,
            "BattingTeam": list,
            "WinningTeam": "last"
        }).reset_index()

        bat1st_wins = 0
        chasing_wins = 0
        no_result = 0

        for _, row in match_outcome.iterrows():
            if len(row["BattingTeam"]) < 2:
                no_result += 1
                continue

            team1 = row["BattingTeam"][0]
            team2 = row["BattingTeam"][1]

            if row["WinningTeam"] == team1:
                bat1st_wins += 1
            elif row["WinningTeam"] == team2:
                chasing_wins += 1
            else:
                no_result += 1

        bat1st_win_pct = round((bat1st_wins / total_matches) * 100, 2) if total_matches else 0
        chasing_win_pct = round((chasing_wins / total_matches) * 100, 2) if total_matches else 0

        avg_1st_innings_score = first_innings.groupby("ID")["total_run"].sum().mean()
        avg_2nd_innings_score = second_innings.groupby("ID")["total_run"].sum().mean()

        total_scores = temp.groupby("ID")["total_run"].sum()
        highest_total = total_scores.max()
        lowest_total = total_scores.min()

        total_fours = temp[temp["batsman_run"] == 4].shape[0]
        total_sixes = temp[temp["batsman_run"] == 6].shape[0]
        total_runs = temp["total_run"].sum()

        # 🆕 Calculate fifties & hundreds
        player_scores = temp.groupby(["ID", "batter"])["batsman_run"].sum()
        total_hundreds = (player_scores >= 100).sum()
        total_fifties = ((player_scores >= 50) & (player_scores < 100)).sum()

        top_batsmen = (
            temp.groupby("batter")["batsman_run"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )

        top_bowlers = (
            temp[temp["isWicketDelivery"] == 1]
            .groupby("bowler")
            .size()
            .sort_values(ascending=False)
            .head(5)
            .reset_index(name="wickets")
        )

        venue_stats.append({
            "Venue": venue,
            "total_matches": total_matches,
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
            "total_hundreds": total_hundreds,   # 🆕
            "total_fifties": total_fifties,     # 🆕
            "top_5_batsmen": top_batsmen.to_dict("records"),
            "top_5_bowlers": top_bowlers.to_dict("records")
        })

    return pd.DataFrame(venue_stats)

if __name__ == "__main__":
    df = pd.read_csv("IPL_Dataset/final_ipl.csv", encoding='ISO-8859-1') 
    venue_df = generate_venue_stats(df)             
    venue_df.to_csv("IPL_Dataset/rag_knowledgebase/venue_stats.csv", index=False)
