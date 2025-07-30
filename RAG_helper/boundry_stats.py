import pandas as pd

def generate_boundary_stats(csv_path):
    df = pd.read_csv(csv_path,encoding='ISO-8859-1')

    # Filter only boundaries
    fours_df = df[df["batsman_run"] == 4]
    sixes_df = df[df["batsman_run"] == 6]

    # Count fours and sixes
    fours = fours_df.groupby(["batter", "BattingTeam", "Season"]).size().reset_index(name="fours")
    sixes = sixes_df.groupby(["batter", "BattingTeam", "Season"]).size().reset_index(name="sixes")

    # Merge both
    boundary_stats = pd.merge(fours, sixes, on=["batter", "BattingTeam", "Season"], how="outer").fillna(0)

    # Convert float to int
    boundary_stats["fours"] = boundary_stats["fours"].astype(int)
    boundary_stats["sixes"] = boundary_stats["sixes"].astype(int)

    # Calculate total runs from boundaries only
    boundary_stats["total_runs"] = boundary_stats["fours"] * 4 + boundary_stats["sixes"] * 6

    # Sort by total runs from boundaries
    boundary_stats = boundary_stats.sort_values(by="total_runs", ascending=False).reset_index(drop=True)

    # Save to CSV
    boundary_stats.to_csv("IPL_Dataset/rag_knowledgebase/boundary_stats1.csv", index=False)

    return boundary_stats

# Example usage:
# generate_boundary_stats("IPL_Dataset/final_ipl.csv")
if __name__=="__main__":
    generate_boundary_stats("IPL_Dataset//final_ipl.csv")