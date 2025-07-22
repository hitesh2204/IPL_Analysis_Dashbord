import pandas as pd

def generate_boundary_stats_csv(ipl):
    try:
        boundary_stats = []

        # Group data by batter and calculate boundaries
        for player in ipl['batter'].unique():
            player_df = ipl[ipl['batter'] == player]
            total_fours = player_df[player_df['batsman_run'] == 4].shape[0]
            total_sixes = player_df[player_df['batsman_run'] == 6].shape[0]
            total_boundaries = total_fours + total_sixes

            boundary_stats.append({
                'player': player,
                'total_fours': total_fours,
                'total_sixes': total_sixes,
                'total_boundaries': total_boundaries
            })

        df = pd.DataFrame(boundary_stats)
        df.sort_values(by='total_boundaries', ascending=False, inplace=True)
        df.to_csv("ipl_dataset//rag_knowledgebase//boundary_stats.csv", index=False)
        print("✅ boundary_stats.csv generated successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    ipl_df = pd.read_csv("IPL_Dataset//ipl_df.csv")  # ✅ Ensure this file path is correct
    generate_boundary_stats_csv(ipl_df)
