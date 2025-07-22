import pandas as pd

def generate_player_stats_csv(ipl):
    player_stats = []

    # Get all unique players from batter + bowler
    batters = set(ipl['batter'].unique())
    bowlers = set(ipl['bowler'].unique())
    all_players = sorted(batters.union(bowlers))

    for player in all_players:
        # Batting stats
        batting_df = ipl[ipl['batter'] == player]
        matches = batting_df['ID'].nunique()
        innings = batting_df['ID'].nunique()
        runs = batting_df['batsman_run'].sum()
        balls = batting_df.shape[0]
        fours = batting_df[batting_df['batsman_run'] == 4].shape[0]
        sixes = batting_df[batting_df['batsman_run'] == 6].shape[0]
        dismissals = ipl[ipl['player_out'] == player]['ID'].nunique()
        strike_rate = round((runs / balls) * 100, 2) if balls > 0 else 0
        avg = round(runs / dismissals, 2) if dismissals > 0 else runs

        match_runs = batting_df.groupby('ID')['batsman_run'].sum()
        highest_score = match_runs.max() if not match_runs.empty else 0
        fifties = match_runs[(match_runs >= 50) & (match_runs < 100)].count()
        hundreds = match_runs[match_runs >= 100].count()

        # Bowling stats
        bowling_df = ipl[(ipl['bowler'] == player) & (ipl['isWicketDelivery'] == 1)]
        total_wickets = bowling_df['player_out'].notna().sum()
        best_bowling = bowling_df.groupby('ID')['player_out'].count().max() if not bowling_df.empty else 0
        five_wkts = (bowling_df.groupby('ID')['player_out'].count() >= 5).sum()

        player_stats.append({
            'Player': player,
            'Matches Played': matches,
            'Innings Played': innings,
            'Total Runs': runs,
            'Total Balls Faced': balls,
            'Total 4s': fours,
            'Total 6s': sixes,
            'Dismissals': dismissals,
            'Batting Average': avg,
            'Strike Rate': strike_rate,
            'Highest Score': highest_score,
            '50s': fifties,
            '100s': hundreds,
            'Total Wickets': total_wickets,
            'Best Bowling': best_bowling,
            '5W Hauls': five_wkts
        })

    player_stats_df = pd.DataFrame(player_stats)
    player_stats_df.to_csv("IPL_Dataset//rag_knowledgebase//player_stats.csv", index=False)
    print("✅ player_stats.csv generated successfully!")

# Run from main
if __name__ == "__main__":
    ipl_df = pd.read_csv("ipl_dataset/ipl_df.csv")
    generate_player_stats_csv(ipl_df)
