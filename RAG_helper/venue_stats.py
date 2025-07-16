import pandas as pd

def generate_venue_stats_csv(ipl):
    venue_stats = []

    for venue in ipl['Venue'].dropna().unique():
        venue_df = ipl[ipl['Venue'] == venue]

        total_matches = venue_df['ID'].nunique()
        total_runs = venue_df['total_run'].sum()
        total_fours = venue_df[venue_df['batsman_run'] == 4].shape[0]
        total_sixes = venue_df[venue_df['batsman_run'] == 6].shape[0]

        # Top 5 batsmen by total runs
        top_batsmen = venue_df.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head(5)
        top_batsmen_str = "; ".join([f"{player}: {runs}" for player, runs in top_batsmen.items()])

        # Top 5 bowlers by dismissals (excluding run outs)
        dismissals = venue_df[(venue_df['isWicketDelivery'] == 1) & (venue_df['player_out'].notnull())]
        top_bowlers = dismissals.groupby('bowler')['player_out'].count().sort_values(ascending=False).head(5)
        top_bowlers_str = "; ".join([f"{bowler}: {wkts}" for bowler, wkts in top_bowlers.items()])

        venue_stats.append({
            'venue': venue,
            'total_matches': total_matches,
            'total_runs': total_runs,
            'total_4s': total_fours,
            'total_6s': total_sixes,
            'top_5_batsmen': top_batsmen_str,
            'top_5_bowlers': top_bowlers_str
        })

    df = pd.DataFrame(venue_stats)
    df.to_csv("ipl_dataset//rag_knowledgebase//venue_stats.csv", index=False)
    print("✅ venue_stats.csv generated successfully!")

# Call this with IPL data
if __name__ == "__main__":
    ipl_df = pd.read_csv("ipl_dataset//final_ipl.csv")  # Adjust path if needed
    generate_venue_stats_csv(ipl_df)
