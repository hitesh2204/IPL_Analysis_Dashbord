import pandas as pd

def generate_player_venue_stats(ipl_df):
    # Filter for fours and sixes
    fours_df = ipl_df[ipl_df['batsman_run'] == 4]
    sixes_df = ipl_df[ipl_df['batsman_run'] == 6]

    # Count of 4s per batter per venue
    fours_count = fours_df.groupby(['batter', 'Venue']).size().reset_index(name='fours')

    # Count of 6s per batter per venue
    sixes_count = sixes_df.groupby(['batter', 'Venue']).size().reset_index(name='sixes')

    # Count of wickets taken per bowler per venue (excluding run outs)
    wickets_df = ipl_df[(ipl_df['isWicketDelivery'] == 1) & (ipl_df['player_out'].notnull())]
    wickets_count = wickets_df.groupby(['bowler', 'Venue']).size().reset_index(name='wickets')
    wickets_count = wickets_count.rename(columns={'bowler': 'batter'})  # Treat bowler as "player" for merging

    # Merge all three stats
    stats = pd.merge(fours_count, sixes_count, on=['batter', 'Venue'], how='outer')
    stats = pd.merge(stats, wickets_count, on=['batter', 'Venue'], how='outer')

    # Fill NaN with 0
    stats[['fours', 'sixes', 'wickets']] = stats[['fours', 'sixes', 'wickets']].fillna(0).astype(int)

    # Save the file
    stats.to_csv("ipl_dataset/rag_knowledgebase/player_venue_stats.csv", index=False)
    print("✅ player_venue_stats.csv generated successfully!")

# Example usage
if __name__ == "__main__":
    ipl_df = pd.read_csv("ipl_dataset/final_ipl.csv",encoding='ISO-8859-1')  # Adjust path if needed
    generate_player_venue_stats(ipl_df)
