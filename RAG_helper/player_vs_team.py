import pandas as pd
from src.data_loader import load_ipl_data

def generate_player_batting_stats(df):
    # Ensure correct column names exist
    required_cols = ['batter', 'Season', 'Venue', 'BattingTeam', 'BowlingTeam', 
                     'batsman_run', 'ballnumber', 'player_out', 'isWicketDelivery', 'ID', 'date']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # Step 1: Calculate per-innings runs for fifties/hundreds & highest score
    innings_runs = df.groupby(['batter', 'Season', 'Venue', 'BowlingTeam', 'ID'])['batsman_run'].sum().reset_index()

    # Step 2: Count fifties and hundreds
    fifties_hundreds = innings_runs.groupby(['batter', 'Season', 'Venue', 'BowlingTeam']).agg(
        fifties=('batsman_run', lambda x: ((x >= 50) & (x < 100)).sum()),
        hundreds=('batsman_run', lambda x: (x >= 100).sum()),
        highest_score=('batsman_run', 'max')
    ).reset_index()

    # Step 3: Main aggregation for totals
    batting_stats = df.groupby(['batter', 'Season', 'Venue', 'BowlingTeam']).agg(
        matches=('date', 'nunique'),          # Unique matches
        innings=('ID', 'nunique'),      # Unique innings
        runs=('batsman_run', 'sum'),
        balls_faced=('ballnumber', 'count'),
        dismissals=('player_out', lambda x: x.notnull().sum()),
        not_outs=('player_out', lambda x: x.isnull().sum()),
        fours=('batsman_run', lambda x: (x == 4).sum()),
        sixes=('batsman_run', lambda x: (x == 6).sum())
    ).reset_index()

    # Step 4: Merge fifties, hundreds, highest score
    batting_stats = batting_stats.merge(fifties_hundreds, 
                                        on=['batter', 'Season', 'Venue', 'BowlingTeam'], 
                                        how='left')

    # Step 5: Calculate average and strike rate
    batting_stats['average'] = batting_stats.apply(
        lambda x: round(x['runs'] / x['dismissals'], 2) if x['dismissals'] > 0 else None, axis=1
    )
    batting_stats['strike_rate'] = batting_stats.apply(
        lambda x: round((x['runs'] / x['balls_faced']) * 100, 2) if x['balls_faced'] > 0 else 0, axis=1
    )

    # Step 6: Save CSV
    batting_stats.to_csv("IPL_Dataset//rag_knowledgebase//player_vs_team_season_venue.csv", index=False)
    print(f" Player batting stats saved to")


# Example usage:
if __name__ == "__main__":
 df = load_ipl_data()
 generate_player_batting_stats(df)
