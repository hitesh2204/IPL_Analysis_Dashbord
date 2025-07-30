import pandas as pd

def generate_team_vs_team_stats(csv_path):
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')

    # Strip whitespace for consistency
    for col in ['Team1', 'Team2', 'WinningTeam', 'BattingTeam', 'batter', 'bowler']:
        df[col] = df[col].astype(str).str.strip()

    # Create sorted team pair identifier (TeamA_vs_TeamB)
    df['team_pair'] = df.apply(lambda x: '_vs_'.join(sorted([x['Team1'], x['Team2']])), axis=1)

    team_stats = []

    for team_pair, group in df.groupby('team_pair'):
        team1, team2 = team_pair.split('_vs_')
        matches = group['ID'].nunique()

        team1_wins = group[group['WinningTeam'] == team1]['ID'].nunique()
        team2_wins = group[group['WinningTeam'] == team2]['ID'].nunique()
        no_result = matches - (team1_wins + team2_wins)

        team1_win_pct = round((team1_wins / matches) * 100, 2) if matches > 0 else 0
        team2_win_pct = round((team2_wins / matches) * 100, 2) if matches > 0 else 0

        # Top Batsman
        batter_stats = group.groupby('batter')['batsman_run'].sum().sort_values(ascending=False)
        top_batsman = batter_stats.index[0] if not batter_stats.empty else None
        top_batsman_runs = batter_stats.iloc[0] if not batter_stats.empty else 0

        # Top Bowler
        bowler_stats = group[group['isWicketDelivery'] == 1].groupby('bowler')['player_out'].count().sort_values(ascending=False)
        top_bowler = bowler_stats.index[0] if not bowler_stats.empty else None
        top_bowler_wickets = bowler_stats.iloc[0] if not bowler_stats.empty else 0

        team_stats.append({
            'team1': team1,
            'team2': team2,
            'matches': matches,
            'team1_wins': team1_wins,
            'team2_wins': team2_wins,
            'no_result': no_result,
            'team1_win_%': team1_win_pct,
            'team2_win_%': team2_win_pct,
            'top_batsman': top_batsman,
            'top_batsman_runs': top_batsman_runs,
            'top_bowler': top_bowler,
            'top_bowler_wickets': top_bowler_wickets
        })

    result_df = pd.DataFrame(team_stats)
    result_df.to_csv("IPL_Dataset/rag_knowledgebase/team_vs_team_summary1.csv", index=False)
    print("✅ team_vs_team_summary.csv generated successfully.")

if __name__ == "__main__":
    generate_team_vs_team_stats("IPL_Dataset/final_ipl.csv")
