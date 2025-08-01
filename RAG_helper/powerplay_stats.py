import pandas as pd

def generate_team_powerplay_stats(csv_path):
    # Load the final IPL dataset
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')

    # Ensure overs are numeric
    df['overs'] = pd.to_numeric(df['overs'], errors='coerce')

    # Filter only Powerplay overs (0.0 to 5.6)
    powerplay_df = df[df['overs'] < 6]

    # Group by match and innings level
    group_cols = ['Season', 'ID', 'innings', 'BattingTeam', 'BowlingTeam', 'Venue']

    powerplay_stats = powerplay_df.groupby(group_cols).agg(
        powerplay_runs=('total_run', 'sum'),
        powerplay_wickets=('isWicketDelivery', 'sum')
    ).reset_index()

    # Rename columns to match your desired format
    powerplay_stats = powerplay_stats.rename(columns={
        'BattingTeam': 'batting_team',
        'BowlingTeam': 'bowling_team',
        'Venue': 'venue'
    })

    # Reorder columns
    powerplay_stats = powerplay_stats[[
        'Season', 'ID', 'innings', 'batting_team', 'bowling_team', 'venue',
        'powerplay_runs', 'powerplay_wickets'
    ]]

    # Save to CSV
    powerplay_stats.to_csv("IPL_Dataset//rag_knowledgebase//powerplay_stats.csv", index=False)

# Run as script
if __name__ == "__main__":
    generate_team_powerplay_stats("IPL_Dataset//final_ipl.csv")
