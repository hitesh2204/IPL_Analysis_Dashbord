import pandas as pd

def generate_head_to_head_csv(ipl_df):
    head_to_head_stats = []

    all_teams = sorted(set(ipl_df['Team1'].unique()) | set(ipl_df['Team2'].unique()))

    # Get unique matches to avoid double counting
    match_info = ipl_df[['Date', 'Team1', 'Team2', 'WinningTeam']].drop_duplicates()

    for i, team1 in enumerate(all_teams):
        for team2 in all_teams[i+1:]:
            # Filter matches between the two teams (any order)
            matches = match_info[
                ((match_info['Team1'] == team1) & (match_info['Team2'] == team2)) |
                ((match_info['Team1'] == team2) & (match_info['Team2'] == team1))
            ]

            total_matches = len(matches)
            if total_matches == 0:
                continue

            team1_wins = (matches['WinningTeam'] == team1).sum()
            team2_wins = (matches['WinningTeam'] == team2).sum()
            no_result = total_matches - (team1_wins + team2_wins)

            team1_win_pct = round((team1_wins / total_matches) * 100, 2)
            team2_win_pct = round((team2_wins / total_matches) * 100, 2)

            # Filter all delivery-level records between these two teams
            mask = (
                ((ipl_df['Team1'] == team1) & (ipl_df['Team2'] == team2)) |
                ((ipl_df['Team1'] == team2) & (ipl_df['Team2'] == team1))
            )
            matchup_deliveries = ipl_df[mask]

            # Top batsman
            batter_stats = matchup_deliveries.groupby('batter')['batsman_run'].sum()
            top_batsman = batter_stats.idxmax()
            top_batsman_runs = batter_stats.max()

            # Top bowler
            dismissals = matchup_deliveries[matchup_deliveries['isWicketDelivery'] == 1]
            bowler_stats = dismissals['bowler'].value_counts()
            top_bowler = bowler_stats.idxmax()
            top_bowler_wickets = bowler_stats.max()

            head_to_head_stats.append({
                'team1': team1,
                'team2': team2,
                'total_matches': total_matches,
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

    df = pd.DataFrame(head_to_head_stats)
    df.to_csv("ipl_dataset/rag_knowledgebase/head_to_head.csv", index=False)
    print("✅ head_to_head.csv generated successfully!")

if __name__ == "__main__":
    ipl = pd.read_csv("IPL_Dataset/ipl_df.csv")
    generate_head_to_head_csv(ipl)
