import pandas as pd
from src.data_loader import load_ipl_data

ipl = load_ipl_data()

def generate_bowler_phasewise_csv(df: pd.DataFrame):
    """
    Generate phase-wise bowling stats per bowler, season, venue, and opponent team.

    Args:
        input_csv (str): Path to the final IPL CSV file
        output_csv (str): Path to save the generated bowler phase-wise CSV
    """
    # --- Define phase function ---
    def get_phase(over):
        if 1 <= over <= 6:
            return "Powerplay"
        elif 7 <= over <= 15:
            return "Middle"
        elif 16 <= over <= 20:
            return "Death"
        else:
            return "Unknown"

    # Ensure overs column is numeric and create phase column
    df["overs"] = pd.to_numeric(df["overs"], errors="coerce")
    df["phase"] = df["overs"].apply(get_phase)

    # --- Bowling stats (per match for aggregation) ---
    bowling_phase = (
        df.groupby(["bowler", "Season", "Venue", "BattingTeam", "phase", "ID"])
        .agg(
            balls_bowled=("valid_ball", "sum"),
            runs_conceded=("total_run", "sum"),
            wickets=("isWicketDelivery", "sum"),
            maidens=("total_run", lambda x: 1 if x.sum() == 0 else 0)  # maiden if 0 runs in match-phase
        )
        .reset_index()
    )

    # --- Aggregate phase-wise ---
    bowler_stats = (
        bowling_phase.groupby(["bowler", "Season", "Venue", "BattingTeam", "phase"])
        .agg(
            matches=("ID", "nunique"),
            balls_bowled=("balls_bowled", "sum"),
            runs=("runs_conceded", "sum"),
            wickets=("wickets", "sum"),
            maidens=("maidens", "sum")
        )
        .reset_index()
    )

    # --- Derived metrics ---
    bowler_stats["overs"] = (bowler_stats["balls_bowled"] / 6).round(1)
    bowler_stats["economy"] = bowler_stats.apply(
        lambda x: round(x["runs"] / x["overs"], 2) if x["overs"] > 0 else 0, axis=1
    )

    # 3W & 5W hauls (per match basis)
    three_wickets = (
        bowling_phase.groupby(["bowler", "Season", "Venue", "BattingTeam", "phase"])["wickets"]
        .apply(lambda x: (x >= 3).sum())
        .reset_index(name="three_wkts")
    )
    five_wickets = (
        bowling_phase.groupby(["bowler", "Season", "Venue", "BattingTeam", "phase"])["wickets"]
        .apply(lambda x: (x >= 5).sum())
        .reset_index(name="five_wkts")
    )

    # Merge
    bowler_stats = bowler_stats.merge(three_wickets, on=["bowler","Season","Venue","BattingTeam","phase"], how="left")
    bowler_stats = bowler_stats.merge(five_wickets, on=["bowler","Season","Venue","BattingTeam","phase"], how="left")

    # Rename columns nicely
    bowler_stats.rename(columns={
        "BattingTeam": "opponent_team",
        "runs": "runs_conceded"
    }, inplace=True)

    # Save CSV
    bowler_stats.to_csv("IPL_Dataset//rag_knowledgebase//bowler_team_phase_season.csv", index=False)
    print(f"Bowler phase-wise CSV generated:")


# Example usage:
if __name__=="__main__":
    generate_bowler_phasewise_csv(ipl)

