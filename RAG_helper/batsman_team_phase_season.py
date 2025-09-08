import pandas as pd
from src.data_loader import load_ipl_data

ipl = load_ipl_data()

def generate_batsman_phasewise_csv(df: pd.DataFrame):
    """
    Generate phase-wise batting stats per batsman, season, venue, and opponent team.
    
    Args:
        input_csv (str): Path to the final IPL CSV file
        output_csv (str): Path to save the generated batsman phase-wise CSV
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

    # --- Batsman stats (per match for aggregation) ---
    batsman_phase = (
        df.groupby(["batter", "Season", "Venue", "BowlingTeam", "phase", "ID"])
        .agg(
            runs=("batsman_run", "sum"),
            balls=("valid_ball", "sum"),
            dismissals=("player_out", lambda x: (x.notna()).sum()),
            fours=("batsman_run", lambda x: (x == 4).sum()),
            sixes=("batsman_run", lambda x: (x == 6).sum())
        )
        .reset_index()
    )

    # Highest score match-wise
    batsman_phase["highest_score"] = batsman_phase["runs"]

    # Mark not outs
    batsman_phase["not_out"] = batsman_phase.apply(
        lambda x: 1 if (x["runs"] > 0 and x["dismissals"] == 0) else 0, axis=1
    )

    # --- Aggregate phase-wise ---
    batsman_stats = (
        batsman_phase.groupby(["batter", "Season", "Venue", "BowlingTeam", "phase"])
        .agg(
            matches=("ID", "nunique"),
            innings=("ID", "count"),
            runs=("runs", "sum"),
            balls=("balls", "sum"),
            dismissals=("dismissals", "sum"),
            not_outs=("not_out", "sum"),
            fours=("fours", "sum"),
            sixes=("sixes", "sum"),
            fifties=("runs", lambda x: (x >= 50).sum()),
            hundreds=("runs", lambda x: (x >= 100).sum()),
            highest_score=("highest_score", "max"),
        )
        .reset_index()
    )

    # Batting metrics
    batsman_stats["average"] = batsman_stats.apply(
        lambda x: round(x["runs"] / x["dismissals"], 2) if x["dismissals"] > 0 else None, axis=1
    )
    batsman_stats["strike_rate"] = batsman_stats.apply(
        lambda x: round((x["runs"] / x["balls"]) * 100, 2) if x["balls"] > 0 else 0, axis=1
    )

    # Save CSV
    batsman_stats.to_csv("IPL_Dataset//rag_knowledgebase//batsman_team_phase_season.csv", index=False)
    print(f"csv generated successfully!")


# Example usage:
if __name__=="__main__":
    generate_batsman_phasewise_csv(ipl)
