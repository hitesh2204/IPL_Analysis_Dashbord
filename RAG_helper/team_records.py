import pandas as pd
from src.data_loader import load_ipl_data

def generate_team_record(df):
   
    # Strip spaces from key columns
    for col in ['BattingTeam', 'bowler', 'batter', 'WinningTeam', 'Team1', 'Team2']:
        df[col] = df[col].str.strip()

    teams = pd.unique(df['Team1'].tolist() + df['Team2'].tolist())
    seasons = df['Season'].unique()
    final_stats = []

    for season in seasons:
        season_df = df[df['Season'] == season]

        for team in teams:
            team_matches = season_df[(season_df['Team1'] == team) | (season_df['Team2'] == team)]
            match_ids = team_matches['ID'].unique()
            total_matches = len(match_ids)

            # Wins
            wins = season_df[season_df['WinningTeam'] == team]['ID'].nunique()

            # No Result
            decided_matches = season_df[~season_df['WinningTeam'].isna()]
            no_result = total_matches - decided_matches[
                (decided_matches['Team1'] == team) | (decided_matches['Team2'] == team)
            ]['ID'].nunique()

            # Losses
            losses = total_matches - wins - no_result

            # Win %
            win_pct = round((wins / total_matches) * 100, 2) if total_matches > 0 else 0.0

            # Runs scored
            team_runs = season_df[season_df['BattingTeam'] == team].groupby('ID')['total_run'].sum().sum()

            # Wickets taken
            wickets_taken = season_df[
                (season_df['isWicketDelivery'] == 1) &
                ((season_df['Team1'] == team) | (season_df['Team2'] == team)) &
                (season_df['BattingTeam'] != team)
            ]
            total_wickets = wickets_taken['player_out'].count()

            # 50s and 100s
            innings_runs = season_df[season_df['BattingTeam'] == team] \
                .groupby(['ID', 'batter'])['batsman_run'].sum().reset_index()
            fifties = innings_runs[(innings_runs['batsman_run'] >= 50) &
                                   (innings_runs['batsman_run'] < 100)].shape[0]
            hundreds = innings_runs[innings_runs['batsman_run'] >= 100].shape[0]

            # 3W and 5W hauls
            bowler_hauls = season_df[
                (season_df['isWicketDelivery'] == 1) & (season_df['BattingTeam'] != team)
            ].groupby(['ID', 'bowler'])['player_out'].count().reset_index()
            threes = bowler_hauls[(bowler_hauls['player_out'] >= 3) &
                                  (bowler_hauls['player_out'] < 5)].shape[0]
            fives = bowler_hauls[bowler_hauls['player_out'] >= 5].shape[0]

            final_stats.append({
                'season': season,
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
    df_result.to_csv("IPL_Dataset//rag_knowledgebase//team_records_seasonwise.csv", index=False)
    print("✅ season-wise team_record.csv generated successfully.")


if __name__ == "__main__":
    ipl = load_ipl_data()
    generate_team_record(ipl)
