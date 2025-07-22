import pandas as pd

def generate_powerplay_stats(input_csv_path: str, output_csv_path: str = "powerplay_stats.csv"):
    """
    Generate powerplay statistics (overs 1 to 6) from IPL ball-by-ball dataset.

    Parameters:
        input_csv_path (str): Path to the IPL dataset CSV file.
        output_csv_path (str): Path where powerplay_stats.csv will be saved.

    Output:
        CSV file containing powerplay stats with columns:
        ['season', 'match_id', 'inning', 'batting_team', 'bowling_team', 'venue',
         'powerplay_runs', 'powerplay_wickets']
    """

    # Step 1: Load dataset
    try:
        df = pd.read_csv(input_csv_path)
    except Exception as e:
        raise FileNotFoundError(f"Failed to load file: {e}")

    # Step 2: Validate required columns
    required_cols = ['ID', 'Season','innings','overs', 'ballnumber',
                     'batsman_run', 'total_run', 'player_out',
                     'BattingTeam', 'BowlingTeam', 'Venue']
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in IPL data: {missing_cols}")

    # Step 3: Filter powerplay overs (1 to 6)
    powerplay_df = df[df['overs'].between(1, 6)]

    # Step 4: Group by season, match, inning, batting team
    grouped = powerplay_df.groupby(
        ['Season', 'ID', 'innings', 'BattingTeam', 'BowlingTeam', 'Venue']
    ).agg(
        powerplay_runs=( 'total_run', 'sum'),
        powerplay_wickets=('player_out', lambda x: x.notnull().sum())
    ).reset_index()

    # Step 5: Rename columns for clarity
    grouped.rename(columns={
        'BattingTeam': 'batting_team',
        'BowlingTeam': 'bowling_team',
        'Venue': 'venue'
    }, inplace=True)

    # Step 6: Save the file
    grouped.to_csv(output_csv_path, index=False)
    print(f"✅ Powerplay stats saved to {output_csv_path}")


if __name__ == "__main__":
    generate_powerplay_stats("IPL_Dataset/ipl_df.csv", "ipl_dataset/rag_knowledgebase/powerplay_stats.csv")
