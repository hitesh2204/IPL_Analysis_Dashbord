import pandas as pd
from src.data_loader import load_ipl_data

def generate_season_summary(df):

    summary = []

    for season in sorted(df['Season'].unique()):
        season_df = df[df['Season'] == season]

        total_matches = season_df['ID'].nunique()
        total_runs = season_df['total_run'].sum()
        total_fours = season_df[season_df['batsman_run'] == 4].shape[0]
        total_sixes = season_df[season_df['batsman_run'] == 6].shape[0]
        total_boundary_runs = (total_fours * 4) + (total_sixes * 6)

        # Highest team total in a match
        match_runs = season_df.groupby(['ID', 'BattingTeam'])['total_run'].sum().reset_index()
        top_score_row = match_runs.loc[match_runs['total_run'].idxmax()]
        highest_score_team = top_score_row['BattingTeam']
        highest_score_runs = top_score_row['total_run']
        highest_score_match_id = top_score_row['ID']

        # Top batsman (Orange Cap)
        top_batsman_stats = season_df.groupby('batter')['batsman_run'].sum().reset_index()
        top_batsman_stats = top_batsman_stats.sort_values(by='batsman_run', ascending=False).head(1)
        top_batsman = top_batsman_stats.iloc[0]['batter']
        top_batsman_runs = top_batsman_stats.iloc[0]['batsman_run']

        # Top bowler (Purple Cap)
        top_bowler_stats = season_df[season_df['isWicketDelivery'] == 1].groupby('bowler')['player_out'].count().reset_index()
        top_bowler_stats = top_bowler_stats.sort_values(by='player_out', ascending=False).head(1)
        top_bowler = top_bowler_stats.iloc[0]['bowler']
        top_bowler_wickets = top_bowler_stats.iloc[0]['player_out']

        # Season winner (last match winner)
        last_match_id = season_df['ID'].max()
        winner_row = season_df[season_df['ID'] == last_match_id]
        winner = winner_row['WinningTeam'].dropna().values
        winner = winner[0] if len(winner) > 0 else 'No Result'

        summary.append({
            'Season': season,
            'Total Matches': total_matches,
            'Total Runs': total_runs,
            'Total Fours': total_fours,
            'Total Sixes': total_sixes,
            'Total Boundary Runs': total_boundary_runs,
            'Highest Score Team': highest_score_team,
            'Highest Score Runs': highest_score_runs,
            'Highest Score Match ID': highest_score_match_id,
            'Top Batsman': top_batsman,
            'Top Batsman Runs': top_batsman_runs,
            'Top Bowler': top_bowler,
            'Top Bowler Wickets': top_bowler_wickets,
            'Orange Cap Winner': top_batsman,  # 🆕
            'Purple Cap Winner': top_bowler,   # 🆕
            'Season Winner': winner
        })

    summary_df = pd.DataFrame(summary)

    # Save to CSV
    summary_df.to_csv("IPL_Dataset//rag_knowledgebase//season_summary_final1.csv", index=False)
    print(f"✅ Season summary saved to:")


# Example usage
if __name__=="__main__":
    ipl = load_ipl_data()
    generate_season_summary(ipl)
