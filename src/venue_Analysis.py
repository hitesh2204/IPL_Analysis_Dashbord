import os
import pandas as pd
import streamlit as st

def venue_analysis_page(ipl):
    st.header("📍 Venue Analysis", divider='rainbow')

    selected_venue = st.session_state.get("selected_venue")
    if not selected_venue:
        venues = sorted(ipl['Venue'].dropna().unique())
        selected_venue = st.selectbox("Select Venue", venues)

    df = ipl[ipl['Venue'] == selected_venue]

    if df.empty:
        st.warning("❌ No data available for this venue.")
        return

    # Image
    venue_img_path = f"venue_images/{selected_venue.replace(' ', '_').replace('/', '_')}.jpeg"
    if os.path.exists(venue_img_path):
        st.image(venue_img_path, width=350, caption=selected_venue)

    # Basic Stats
    st.subheader(f"🏟️ Stats for {selected_venue}")
    total_matches = df['ID'].nunique()
    total_runs = df['total_run'].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Matches", total_matches)
    col2.metric("Total Runs", total_runs)

    col3, col4 = st.columns(2)
    col3.metric("Total Fours", df[df['batsman_run'] == 4].shape[0])
    col4.metric("Total Sixes", df[df['batsman_run'] == 6].shape[0])

    # ✅ Matches played by each team at this venue (correct logic)
    st.subheader("🎯 Matches Played by Teams at this Venue")

    # Combine both Team1 and Team2 for proper match counts
    team_matches_df = pd.concat([
        df[['ID', 'Team1']].rename(columns={'Team1': 'Team'}),
        df[['ID', 'Team2']].rename(columns={'Team2': 'Team'})
    ])

    # Drop duplicates: one match per team
    team_matches_df = team_matches_df.drop_duplicates()

    # Count matches per team
    team_match_counts = team_matches_df.groupby('Team')['ID'].nunique().reset_index()
    team_match_counts.columns = ['Team', 'Matches Played']
    team_match_counts = team_match_counts.sort_values(by='Matches Played', ascending=False)

    st.dataframe(team_match_counts, use_container_width=True)

    sum_team_matches = team_match_counts['Matches Played'].sum()
    expected = total_matches * 2

    if sum_team_matches == expected:
        st.success(f"✅ Verified: {total_matches} total matches → {sum_team_matches} team appearances.")
    else:
        st.warning(f"⚠️ Mismatch: {total_matches} matches ≠ {sum_team_matches} team match counts")


    # 🧢 Top Run Scorers
    st.subheader("🧢 Top Run Scorers")
    run_col = 'batsman_run' if 'batsman_run' in df.columns else 'total_run'
    top_scorers = df.groupby('batter')[run_col].sum().sort_values(ascending=False).head(5).reset_index()
    top_scorers.columns = ['Batter', 'Runs']
    st.dataframe(top_scorers, use_container_width=True)

    # 🎯 Top Wicket Takers
    st.subheader("🎯 Top Wicket Takers")
    if {'isWicketDelivery', 'bowler', 'player_out'}.issubset(df.columns):
        top_wickets = df[df['isWicketDelivery'] == 1].groupby('bowler')['player_out'].count() \
            .sort_values(ascending=False).head(5).reset_index()
        top_wickets.columns = ['Bowler', 'Wickets']
        st.dataframe(top_wickets, use_container_width=True)
    else:
        st.info("Wicket data not available in the dataset.")

    # 🔥 Top Boundary Hitters
    st.subheader("🔥 Top Boundary Hitters")
    boundary_df = df[df['batsman_run'].isin([4, 6])]
    boundary_counts = boundary_df.groupby(['batter', 'batsman_run']).size().unstack(fill_value=0)
    boundary_counts['Total Boundaries'] = boundary_counts.get(4, 0) + boundary_counts.get(6, 0)
    top_boundary_hitters = boundary_counts.sort_values(by='Total Boundaries', ascending=False).head(5)

    st.dataframe(
        top_boundary_hitters[['Total Boundaries', 4, 6]].rename(columns={4: "Fours", 6: "Sixes"}),
        use_container_width=True
    )


# 🧠-GENAI FUNCTION — Used by LangChain Agent
def get_venue_summary(ipl, venue_query: str) -> str:
    venue = venue_query.strip()

    df = ipl[ipl['Venue'].str.lower() == venue.lower()]
    if df.empty:
        return f"No data found for venue '{venue}'."

    total_matches = df['ID'].nunique()

    # Innings-wise average scores
    first_innings = df[df['innings'] == 1].groupby('ID')['total_run'].sum()
    second_innings = df[df['innings'] == 2].groupby('ID')['total_run'].sum()
    avg_score_1 = first_innings.mean()
    avg_score_2 = second_innings.mean()

    # Total runs, 4s, and 6s
    total_runs = df['batsman_run'].sum()
    total_fours = df[df['batsman_run'] == 4].shape[0]
    total_sixes = df[df['batsman_run'] == 6].shape[0]

    # Match win analysis
    match_results = df.groupby('ID').agg({
        'BattingTeam': 'first',
        'WinningTeam': 'first',
        'innings': 'max'
    }).reset_index()
    bat_first_win = match_results[match_results['WinningTeam'] == match_results['BattingTeam']].shape[0]
    chase_win = total_matches - bat_first_win

    # Top 5 teams by win
    team_wins = df.groupby('WinningTeam')['ID'].nunique().sort_values(ascending=False).head(3)

    # Top 5 batsmen
    top_batsmen = df.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head(5)

    # Top 5 bowlers
    top_bowlers = df[df['isWicketDelivery'] == 1].groupby('bowler')['player_out'].count().sort_values(ascending=False).head(5)

    return (
        f"🏟️ **Venue Summary: {venue}**\n\n"
        f"• Total Matches: {total_matches}\n"
        f"• Avg 1st Innings Score: {avg_score_1:.2f}\n"
        f"• Avg 2nd Innings Score: {avg_score_2:.2f}\n"
        f"• Total Runs Scored: {total_runs}\n"
        f"• Total Fours: {total_fours} | Total Sixes: {total_sixes}\n"
        f"• Bat First Wins: {bat_first_win} | Chasing Wins: {chase_win}\n\n"

        f"🏆 **Top Teams (by Wins)**:\n" +
        "\n".join([f"- {team}: {wins} wins" for team, wins in team_wins.items()]) + "\n\n"

        f"🔥 **Top 5 Batsmen at {venue}**:\n" +
        "\n".join([f"- {batsman}: {runs} runs" for batsman, runs in top_batsmen.items()]) + "\n\n"

        f"🎯 **Top 5 Bowlers at {venue}**:\n" +
        "\n".join([f"- {bowler}: {wkts} wickets" for bowler, wkts in top_bowlers.items()])
    )
