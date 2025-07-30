import pandas as pd

def generate_team_record(csv_path):
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')

    # Strip spaces
    for col in ['BattingTeam', 'bowler', 'batter', 'WinningTeam', 'Team1', 'Team2']:
        df[col] = df[col].str.strip()

    teams = pd.unique(df['Team1'].tolist() + df['Team2'].tolist())
    final_stats = []

    for team in teams:
        team_matches = df[(df['Team1'] == team) | (df['Team2'] == team)]
        match_ids = team_matches['ID'].unique()
        total_matches = len(match_ids)

        # Wins
        wins = df[df['WinningTeam'] == team]['ID'].nunique()

        # No Result
        decided_matches = df[~df['WinningTeam'].isna()]
        no_result = total_matches - decided_matches[
            (decided_matches['Team1'] == team) | (decided_matches['Team2'] == team)
        ]['ID'].nunique()

        losses = total_matches - wins - no_result
        win_pct = round((wins / total_matches) * 100, 2) if total_matches > 0 else 0.0

        # Runs scored
        team_runs = df[df['BattingTeam'] == team].groupby('ID')['total_run'].sum().sum()

        # Wickets taken
        wickets_taken = df[
            (df['isWicketDelivery'] == 1) &
            ((df['Team1'] == team) | (df['Team2'] == team)) &
            (df['BattingTeam'] != team)
        ]
        total_wickets = wickets_taken['player_out'].count()

        # 50s and 100s
        innings_runs = df[df['BattingTeam'] == team].groupby(['ID', 'batter'])['batsman_run'].sum().reset_index()
        fifties = innings_runs[(innings_runs['batsman_run'] >= 50) & (innings_runs['batsman_run'] < 100)].shape[0]
        hundreds = innings_runs[innings_runs['batsman_run'] >= 100].shape[0]

        # 3W and 5W hauls
        bowler_hauls = df[
            (df['isWicketDelivery'] == 1) & (df['BattingTeam'] != team)
        ].groupby(['ID', 'bowler'])['player_out'].count().reset_index()
        threes = bowler_hauls[(bowler_hauls['player_out'] >= 3) & (bowler_hauls['player_out'] < 5)].shape[0]
        fives = bowler_hauls[bowler_hauls['player_out'] >= 5].shape[0]

        final_stats.append({
            'team': team,
            'matches_played': total_matches,
            'wins': wins,
            'losses': losses,
            'no_result': no_result,
            'win_%': win_pct,
            'total_runs_scored': team_runs,
            'total_wickets_taken': total_wickets,
            '50s': fifties,
            '100s': hundreds,
            '3w_hauls': threes,
            '5w_hauls': fives
        })

    df_result = pd.DataFrame(final_stats)
    df_result.to_csv("IPL_Dataset//rag_knowledgebase//team_records1.csv", index=False)
    print("✅ team_record.csv generated successfully.")

if __name__ == "__main__":
    generate_team_record("IPL_Dataset//final_ipl.csv")
