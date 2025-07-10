import streamlit as st
import pandas as pd
import os
from PIL import Image
import matplotlib.pyplot as plt

def venue_analysis_page(ipl):
    st.header("📍 Venue Analysis", divider='rainbow')

    # 🔄 Hybrid Mode: Use session_state if present
    selected_venue = st.session_state.get("selected_venue")

    # Fallback to dropdown if not passed by LLM
    if not selected_venue:
        venues = sorted(ipl['Venue'].dropna().unique())
        selected_venue = st.selectbox("Select Venue", venues)

    # Filter matches at selected venue
    df = ipl[ipl['Venue'] == selected_venue]

    if df.empty:
        st.warning("❌ No data available for this venue.")
        return

    # Optional image display
    venue_img_path = f"venue_images/{selected_venue.replace(' ', '_').replace('/', '_')}.jpeg"
    if os.path.exists(venue_img_path):
        st.image(venue_img_path, width=350, caption=selected_venue)

    # Key stats
    st.subheader(f"🏟️ Stats for {selected_venue}")
    total_matches = df['ID'].nunique()
    total_runs = df['total_run'].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Matches", total_matches)
    col2.metric("Total Runs", total_runs)

    # Total 4s and 6s
    col3, col4 = st.columns(2)
    col3.metric("Total Fours", df[df['batsman_run'] == 4].shape[0])
    col4.metric("Total Sixes", df[df['batsman_run'] == 6].shape[0])

    # Top Teams
    st.subheader("🎯 Top Teams at this Venue")
    team_counts = pd.concat([df['Team1'], df['Team2']]).value_counts().reset_index()
    team_counts.columns = ['Team', 'Matches Played']
    st.dataframe(team_counts, use_container_width=True)

    # Top Run Scorers
    st.subheader("🧢 Top Run Scorers")
    run_col = 'batsman_run' if 'batsman_run' in df.columns else 'total_run'
    top_scorers = df.groupby('batter')[run_col].sum().sort_values(ascending=False).head(5).reset_index()
    top_scorers.columns = ['Batter', 'Runs']
    st.dataframe(top_scorers, use_container_width=True)

    # Top Wicket Takers
    st.subheader("🎯 Top Wicket Takers")
    if {'isWicketDelivery', 'bowler', 'player_out'}.issubset(df.columns):
        top_wickets = df[df['isWicketDelivery'] == 1].groupby('bowler')['player_out'].count() \
            .sort_values(ascending=False).head(5).reset_index()
        top_wickets.columns = ['Bowler', 'Wickets']
        st.dataframe(top_wickets, use_container_width=True)
    else:
        st.info("Wicket data not available in the dataset.")

    # Top Boundary Hitters
    st.subheader("🔥 Top Boundary Hitters")
    boundary_df = df[df['batsman_run'].isin([4, 6])]
    boundary_counts = boundary_df.groupby(['batter', 'batsman_run']).size().unstack(fill_value=0)
    boundary_counts['Total Boundaries'] = boundary_counts.get(4, 0) + boundary_counts.get(6, 0)
    top_boundary_hitters = boundary_counts.sort_values(by='Total Boundaries', ascending=False).head(5)

    st.dataframe(
        top_boundary_hitters[['Total Boundaries', 4, 6]].rename(columns={4: "Fours", 6: "Sixes"}),
        use_container_width=True
    )
