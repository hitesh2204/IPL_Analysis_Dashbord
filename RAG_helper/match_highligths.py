import pandas as pd

def generate_match_highlights(ipl_df):
    highlights = []

    grouped = ipl_df.groupby("ID")

    for match_id, group in grouped:
        match_info = group.iloc[0]  # First row of the match
        total_runs = group["total_run"].sum()
        total_wickets = group["player_out"].notna().sum()
        total_sixes = group[group["batsman_run"] == 6].shape[0]
        total_fours = group[group["batsman_run"] == 4].shape[0]

        highlights.append({
            "match_id": match_id,
            "season": match_info.get("Season", ""),
            "date": match_info.get("Date", ""),
            "venue": match_info.get("Venue", ""),
            "team1": match_info.get("Team1", ""),
            "team2": match_info.get("Team2", ""),
            "toss_winner": match_info.get("TossWinner", ""),
            "toss_decision": match_info.get("TossDecision", ""),
            "winner": match_info.get("WinningTeam", ""),
            "win_by_runs": match_info.get("win_by_runs", 0),
            "win_by_wickets": match_info.get("win_by_wickets", 0),
            "player_of_match": match_info.get("Player_of_Match", ""),
            "total_runs": total_runs,
            "total_wickets": total_wickets,
            "total_sixes": total_sixes,
            "total_fours": total_fours
        })

    df = pd.DataFrame(highlights)
    df.to_csv("ipl_dataset//rag_knowledgebase//match_highlights.csv", index=False)
    print("✅ match_highlights.csv generated successfully!")

# Run this function with your loaded IPL data
if __name__ == "__main__":
    df = pd.read_csv("ipl_dataset//final_ipl.csv",encoding='ISO-8859-1')
    generate_match_highlights(df)
