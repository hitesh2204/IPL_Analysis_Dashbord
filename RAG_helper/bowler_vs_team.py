import pandas as pd

def generate_bowler_vs_team_csv(ipl):
    bowler_stats = []

    # Determine which column represents the batting team
    if 'BattingTeam' in ipl.columns:
        batting_col = 'BattingTeam'
    elif 'Team1' in ipl.columns:
        batting_col = 'Team1'  # Fallback
    else:
        raise KeyError("❌ 'BattingTeam' or 'Team1' column not found in dataset.")

    for bowler in ipl['bowler'].unique():
        bowler_df = ipl[ipl['bowler'] == bowler]

        for team in bowler_df[batting_col].unique():
            vs_team_df = bowler_df[bowler_df[batting_col] == team]
            total_balls = vs_team_df.shape[0]
            total_runs = vs_team_df['total_run'].sum()

            # Only valid wicket deliveries count for wicket-taking
            wicket_df = vs_team_df[(vs_team_df['isWicketDelivery'] == 1) & (vs_team_df['player_out'].notnull())]
            total_wickets = wicket_df.shape[0]

            # Best bowling = max wickets in a single match
            best_bowling_df = wicket_df.groupby('ID')['player_out'].count()
            best_figures = best_bowling_df.max() if not best_bowling_df.empty else 0

            # 3W and 5W hauls
            threes = best_bowling_df[best_bowling_df >= 3].count()
            fives = best_bowling_df[best_bowling_df >= 5].count()

            economy = round((total_runs / total_balls) * 6, 2) if total_balls > 0 else 0

            bowler_stats.append({
                'bowler': bowler,
                'opposition': team,
                'balls_bowled': total_balls,
                'runs_conceded': total_runs,
                'wickets': total_wickets,
                'best_figures': best_figures,
                'economy': economy,
                '3W_hauls': threes,
                '5W_hauls': fives
            })

    df = pd.DataFrame(bowler_stats)
    df.to_csv("ipl_dataset//rag_knowledgebase//bowler_vs_team.csv", index=False)
    print("✅ bowler_vs_team.csv generated successfully!")

# Run the script directly
if __name__ == "__main__":
    ipl = pd.read_csv("ipl_dataset//final_ipl.csv")
    generate_bowler_vs_team_csv(ipl)
