import pandas as pd

def generate_player_vs_team_csv(ipl):
    player_vs_team_stats = []

    # Detect correct column for bowling team
    if 'BowlingTeam' in ipl.columns:
        bowling_col = 'BowlingTeam'
    elif 'Team2' in ipl.columns:
        bowling_col = 'Team2'  # fallback
    else:
        raise KeyError("❌ Neither 'BowlingTeam' nor 'Team2' column found in dataset.")

    for player in ipl['batter'].unique():
        player_df = ipl[ipl['batter'] == player]

        for opposition in player_df[bowling_col].unique():
            opp_df = player_df[player_df[bowling_col] == opposition]
            runs = opp_df['batsman_run'].sum()
            balls = opp_df.shape[0]
            outs = opp_df[opp_df['player_out'] == player].shape[0]
            strike_rate = round((runs / balls) * 100, 2) if balls > 0 else 0

            match_runs = opp_df.groupby('ID')['batsman_run'].sum()
            highest_score = match_runs.max() if not match_runs.empty else 0
            fifties = match_runs[(match_runs >= 50) & (match_runs < 100)].count()
            hundreds = match_runs[match_runs >= 100].count()

            player_vs_team_stats.append({
                'batter': player,
                'opposition': opposition,
                'matches': opp_df['ID'].nunique(),
                'runs': runs,
                'balls': balls,
                'strike_rate': strike_rate,
                'dismissals': outs,
                'highest_score': highest_score,
                '50s': fifties,
                '100s': hundreds
            })

    df = pd.DataFrame(player_vs_team_stats)
    df.to_csv("ipl_dataset//rag_knowledgebase//player_vs_team.csv", index=False)
    print("✅ player_vs_team.csv generated successfully!")

# Run directly
if __name__ == "__main__":
    ipl = pd.read_csv("ipl_dataset//ipl_df.csv")
    generate_player_vs_team_csv(ipl)
