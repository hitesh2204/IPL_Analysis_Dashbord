import pandas as pd
from src.data_loader import load_ipl_data

def generate_bowling_stats(df):
   
    # Ensure player_out and bowler columns exist
    if 'player_out' not in df.columns or 'bowler' not in df.columns:
        raise ValueError("Input CSV must contain 'player_out' and 'bowler' columns.")

    # Create a wickets flag
    df['wicket'] = df['isWicketDelivery'].apply(lambda x: 1 if x == 1 else 0)

    # Convert overs from ball counts
    df['over_number'] = df.groupby(['ID', 'bowler']).cumcount() // 6 + 1

    # Group by player, season, venue, opponent
    grouped = df.groupby(['bowler', 'Season', 'Venue', 'BattingTeam'])

    # Aggregate stats
    stats = grouped.agg(
        matches_played=('ID', 'nunique'),
        wickets=('wicket', 'sum'),
        runs_conceded=('total_run', 'sum'),
        balls_bowled=('isWicketDelivery', 'count'),
        maidens=('over_number', lambda x: (x.value_counts() == 0).sum())  # placeholder
    ).reset_index()

    # Calculate overs bowled
    stats['overs'] = stats['balls_bowled'] / 6
    stats['economy'] = stats['runs_conceded'] / stats['overs']
    
    # Add three_wicket_hauls and five_wicket_hauls
    haul_data = df.groupby(['bowler', 'Season', 'Venue', 'BattingTeam', 'ID'])['wicket'].sum().reset_index()
    haul_counts = haul_data.groupby(['bowler', 'Season', 'Venue', 'BattingTeam']).agg(
        three_wk_hauls=('wicket', lambda x: (x >= 3).sum()),
        five_wk_hauls=('wicket', lambda x: (x >= 5).sum())
    ).reset_index()

    # Merge haul counts into stats
    stats = stats.merge(haul_counts, on=['bowler', 'Season', 'Venue', 'BattingTeam'], how='left')

    # Fill NaN values
    stats = stats.fillna(0)

    # Rename columns for clarity
    stats = stats.rename(columns={
        'bowler': 'player_name',
        'Season': 'season',
        'Venue': 'venue',
        'BattingTeam': 'opponent_team'
    })

    # Save to CSV
    stats.to_csv("IPL_Dataset//rag_knowledgebase//bolwer_vs_team_season_venue.csv", index=False)
    print(f"✅ Bowling stats saved to")


# Example usage:
if __name__ == "__main__":
    ipl = load_ipl_data()
    generate_bowling_stats(ipl)
