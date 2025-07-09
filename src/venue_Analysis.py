import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

def venue_advanced_stats(ipl):
    st.header("📍 Venue Analysis", divider='rainbow')

    # ✅ Step 1: Select venue
    venues = sorted(ipl['Venue'].dropna().unique())
    selected_venue = st.selectbox("Select Venue", venues)

    # ✅ Step 2: Filter by venue
    df = ipl[ipl['Venue'] == selected_venue]

    # ✅ Step 3: Debug data check
    if df.empty:
        st.warning("❌ No data available for this venue.")
        return

    # ✅ Step 4: Optional image
    venue_img_path = f"venue_images/{selected_venue.replace(' ', '_').replace('/', '_')}.jpeg"
    if os.path.exists(venue_img_path):
        st.image(venue_img_path, width=350, caption=selected_venue)

    # ✅ Step 5: Stats
    st.subheader(f"🏟️ Stats for {selected_venue}")
    total_matches = df['ID'].nunique()
    total_runs = df['total_run'].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Matches", total_matches)
    col2.metric("Total Runs", total_runs)

    # ✅ Step 6: Total 4s and 6s at the venue
    total_fours = df[df['batsman_run'] == 4].shape[0]
    total_sixes = df[df['batsman_run'] == 6].shape[0]

    col3, col4 = st.columns(2)
    col3.metric("Total Fours", total_fours)
    col4.metric("Total Sixes", total_sixes)

    # ✅ Step 7: Top Teams at this Venue (corrected logic)
    st.subheader("🎯 Top Teams at this Venue")
    venue_matches = df[['ID', 'Team1', 'Team2']].drop_duplicates()
    team_counts = pd.melt(venue_matches, id_vars='ID', value_vars=['Team1', 'Team2'],
                          var_name='TeamType', value_name='Team')
    top_teams = team_counts['Team'].value_counts().reset_index()
    top_teams.columns = ['Team', 'Matches Played']
    st.dataframe(top_teams, use_container_width=True)

    # ✅ Step 8: Top Run Scorers
    st.subheader("🧢 Top Run Scorers")
    run_col = 'batsman_run' if 'batsman_run' in df.columns else 'total_run'
    top_scorers = df.groupby('batter')[run_col].sum().sort_values(ascending=False).head(5).reset_index()
    top_scorers.columns = ['Batter', 'Runs']
    st.dataframe(top_scorers, use_container_width=True)

    # ✅ Step 9: Top Wicket Takers
    st.subheader("🎯 Top Wicket Takers")
    if {'isWicketDelivery', 'bowler', 'player_out'}.issubset(df.columns):
        top_wickets = df[df['isWicketDelivery'] == 1].groupby('bowler')['player_out'] \
            .count().sort_values(ascending=False).head(5).reset_index()
        top_wickets.columns = ['Bowler', 'Wickets']
        st.dataframe(top_wickets, use_container_width=True)
    else:
        st.info("Wicket data not available in the dataset.")

    # ✅ Step 10: Top Boundary Hitters
    st.subheader("🔥 Top Boundary Hitters")
    boundary_df = df[df['batsman_run'].isin([4, 6])]
    boundary_counts = boundary_df.groupby(['batter', 'batsman_run']).size().unstack(fill_value=0)
    boundary_counts['Total Boundaries'] = boundary_counts.get(4, 0) + boundary_counts.get(6, 0)
    top_boundary_hitters = boundary_counts.sort_values(by='Total Boundaries', ascending=False).head(5)

    st.dataframe(
        top_boundary_hitters[['Total Boundaries', 4, 6]].rename(columns={4: "Fours", 6: "Sixes"}),
        use_container_width=True
    )
