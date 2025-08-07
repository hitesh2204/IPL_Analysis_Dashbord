import pandas as pd
from src.data_loader import load_ipl_data


def get_phase_wise_performance(player_name, phase, season, df):
    # Phase mapping based on overs
    phase_map = {
        'powerplay': (0, 5),
        'middle': (6, 15),
        'death': (16, 20)
    }

    phase = phase.lower()
    if phase not in phase_map:
        return f"Invalid phase: {phase}. Choose from Powerplay, Middle, or Death."

    over_start, over_end = phase_map[phase]

    if season:
        df = df[df["Season"] == season]

    # Filter by overs
    df_phase = df[(df["overs"] >= over_start) & (df["overs"] <= over_end)]

    # Batting
    batting_df = df_phase[df_phase["batter"] == player_name]
    runs = batting_df["batsman_run"].sum()
    balls = batting_df.shape[0]
    dismissals = batting_df[batting_df["player_out"] == player_name].shape[0]

    # Bowling
    bowling_df = df_phase[df_phase["bowler"] == player_name]
    balls_bowled = bowling_df.shape[0]
    wickets = bowling_df[bowling_df["isWicketDelivery"] == 1].shape[0]
    runs_conceded = bowling_df["total_run"].sum()

    result = f"📊 {player_name}'s performance in **{phase.title()} Overs**"
    result += f"\n\n🟢 **Batting:**\n- Runs: {runs}\n- Balls: {balls}\n- Dismissals: {dismissals}"
    result += f"\n\n🔵 **Bowling:**\n- Balls Bowled: {balls_bowled}\n- Runs Conceded: {runs_conceded}\n- Wickets: {wickets}"

    if season:
        result += f"\n\n🗓️ Season: {season}"

    return result

