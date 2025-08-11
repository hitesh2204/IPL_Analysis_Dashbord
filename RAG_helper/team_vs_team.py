import pandas as pd
from src.data_loader import load_ipl_data

def generate_team_vs_team_stats(df):

    # Ensure numeric types
    df['batsman_run'] = pd.to_numeric(df['batsman_run'], errors='coerce').fillna(0)
    df['total_run'] = pd.to_numeric(df['total_run'], errors='coerce').fillna(0)
    df['isWicketDelivery'] = df['isWicketDelivery'].astype(int)

    # Clean text columns
    for col in ['Team1', 'Team2', 'WinningTeam', 'BattingTeam', 'batter', 'bowler']:
        df[col] = df[col].astype(str).str.strip()

    # Extra columns
    df['four'] = (df['batsman_run'] == 4).astype(int)
    df['six'] = (df['batsman_run'] == 6).astype(int)
    df['dot_ball'] = (df['total_run'] == 0).astype(int)

    wicket_types = ['bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
    df['isBowlerWicket'] = df['player_out'].notnull() & df['kind'].isin(wicket_types)

    # Create team pair
    df['team_pair'] = df.apply(lambda x: '_vs_'.join(sorted([x['Team1'], x['Team2']])), axis=1)

    team_stats = []

    for (season, team_pair), group in df.groupby(['Season', 'team_pair']):
        team1, team2 = team_pair.split('_vs_')
        matches = group['ID'].nunique()

        team1_wins = group[group['WinningTeam'] == team1]['ID'].nunique()
        team2_wins = group[group['WinningTeam'] == team2]['ID'].nunique()
        no_result = matches - (team1_wins + team2_wins)

        team1_win_pct = round((team1_wins / matches) * 100, 2) if matches else 0
        team2_win_pct = round((team2_wins / matches) * 100, 2) if matches else 0

        # Batting records
        match_scores = group.groupby(['ID', 'BattingTeam'])['total_run'].sum()
        highest_score = match_scores.max()
        total_50s = (match_scores.between(50, 99)).sum()
        total_100s = (match_scores >= 100).sum()

        total_fours = group['four'].sum()
        total_sixes = group['six'].sum()

        balls_faced = len(group)
        total_runs = group['total_run'].sum()
        strike_rate = round((total_runs / balls_faced) * 100, 2) if balls_faced else 0
        run_rate = round(total_runs / (balls_faced / 6), 2) if balls_faced else 0

        # Bowling records
        bowler_wickets = group[group['isBowlerWicket']].groupby('bowler').size()
        most_wickets = bowler_wickets.max() if not bowler_wickets.empty else 0
        top_bowler = bowler_wickets.idxmax() if not bowler_wickets.empty else None

        best_figures = group.groupby(['ID', 'bowler'])['isBowlerWicket'].sum().max()
        total_dot_balls = group['dot_ball'].sum()

        total_balls_bowled = len(group)
        runs_conceded = group['total_run'].sum()
        economy_rate = round(runs_conceded / (total_balls_bowled / 6), 2) if total_balls_bowled else 0

        three_wicket_hauls = (group.groupby(['ID', 'bowler'])['isBowlerWicket'].sum() >= 3).sum()
        five_wicket_hauls = (group.groupby(['ID', 'bowler'])['isBowlerWicket'].sum() >= 5).sum()

        # Top batsman
        batter_stats = group.groupby('batter')['batsman_run'].sum().sort_values(ascending=False)
        top_batsman = batter_stats.index[0] if not batter_stats.empty else None
        top_batsman_runs = batter_stats.iloc[0] if not batter_stats.empty else 0

        team_stats.append({
            'season': season,
            'team1': team1,
            'team2': team2,
            'matches': matches,
            'team1_wins': team1_wins,
            'team2_wins': team2_wins,
            'no_result': no_result,
            'team1_win_%': team1_win_pct,
            'team2_win_%': team2_win_pct,

            # Batting
            'highest_score': highest_score,
            'total_50s': total_50s,
            'total_100s': total_100s,
            'total_fours': total_fours,
            'total_sixes': total_sixes,
            'strike_rate': strike_rate,
            'run_rate': run_rate,

            # Bowling
            'most_wickets': most_wickets,
            'top_bowler': top_bowler,
            'best_figures': best_figures,
            'economy_rate': economy_rate,
            'total_dot_balls': total_dot_balls,
            'three_wicket_hauls': three_wicket_hauls,
            'five_wicket_hauls': five_wicket_hauls,

            # Top batter
            'top_batsman': top_batsman,
            'top_batsman_runs': top_batsman_runs
        })

    result_df = pd.DataFrame(team_stats)
    result_df.to_csv("IPL_Dataset/rag_knowledgebase/team_vs_team_season.csv", index=False)
    print("✅ team_vs_team_seasonwise.csv generated successfully.")

if __name__ == "__main__":
    ipl = load_ipl_data()
    generate_team_vs_team_stats(ipl)
