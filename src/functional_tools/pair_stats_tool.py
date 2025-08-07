# src/functional_tools/pair_stats_tool.py

from src.data_loader import load_ipl_data
ipl=load_ipl_data()

def get_pair_stats(player1, player2, season=None):
    df = ipl.copy()

    if season:
        df = df[df["Season"] == int(season)]

    # Filter for both players involved in same partnership
    pair_df = df[(df["batter"].isin([player1, player2])) & (df["non-striker"].isin([player1, player2]))]

    if pair_df.empty:
        return f"No partnership data found for {player1} and {player2} in season {season or 'all seasons'}."

    total_runs = pair_df["batsman_run"].sum()
    balls_faced = pair_df.shape[0]
    avg_runs_per_ball = round(total_runs / balls_faced, 2) if balls_faced else 0

    pair_stats = f"""👬 **Pair Stats: {player1} & {player2}**
                    - Total Runs Together: {total_runs}
                    - Balls Faced Together: {balls_faced}
                    - Average Runs per Ball: {avg_runs_per_ball}
                    - Matches Played Together: {pair_df["ID"].nunique()}
                    - Season: {season or 'Overall'}"""

    return pair_stats


