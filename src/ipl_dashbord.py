import streamlit as st
import pandas as pd
from PIL import Image
from src.utils import autoplay_video, get_image_path
from src.data_loader import load_ipl_data
from src.plots import plot_run_distribution, plot_ball_timeline
from src.leaderboard import leaderboard_dashboard
from src.player_summary import player_summary_page
from src.player_comparison import player_detailed_comparison
from src.venue_analysis import venue_analysis_page
from Chatbot.genai_chat import genai_chat_tab
from src.team_vs_team import team_vs_team_analysis
from src.tournament_summary import tournament_summary_page
from logger import setup_logger
import matplotlib.pyplot as plt
import os

logger = setup_logger()

class IPLDashboard:
    def __init__(self):
        try:
            logger.info("Initializing IPLDashboard and loading data...")
            self.ipl = load_ipl_data()

            self.ipl['Venue'] = self.ipl['Venue'].astype(str).str.strip()
            self.ipl['batter'] = self.ipl['batter'].astype(str).str.strip()
            self.ipl['bowler'] = self.ipl['bowler'].astype(str).str.strip()
            self.ipl['player_out'] = self.ipl['player_out'].astype(str).str.strip()

            self.batsmen = sorted(self.ipl['batter'].unique())
            self.bowlers = sorted(self.ipl['bowler'].unique())
            logger.info("Initialization completed successfully.")

        except Exception as e:
            logger.exception("Error during IPLDashboard initialization.")
            st.error("Failed to initialize the dashboard. Please check the logs.")

    def show_overview(self):
        try:
            logger.info("Displaying IPL overview.")
            pic = Image.open("image-video/hitu.jpeg")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.title("IPL-Insights-by-Hitesh")
            with col2:
                st.image(pic, width=120)

            st.title(":red[IPL]:green[-]:blue[Analysis] :sunglasses:")

            image = Image.open("image-video/IPL1-2024-Squad.jpg")
            st.image(image, caption='All IPL teams-captains')

            autoplay_video("image-video/ipl_video.mp4")
            st.balloons()

            trophy_path = "image-video/ipl_trophy.jpeg"
            if os.path.exists(trophy_path):
                st.image(trophy_path, caption='🏆 IPL Trophy', width=300)

            st.subheader("🏆 IPL Trophy Winners (2008–2024)")
            trophy_data = {
                "Team": [
                    "Mumbai Indians", "Chennai Super Kings", "Kolkata Knight Riders",
                    "Sunrisers Hyderabad", "Rajasthan Royals", "Deccan Chargers",
                    "Gujarat Titans","Royal Challengers Bangalore"
                ],
                "Titles Won": [5, 5, 3, 1, 1, 1, 1, 1],
                "Winning Years": [
                    "2013, 2015, 2017, 2019, 2020",
                    "2010, 2011, 2018, 2021, 2023",
                    "2012, 2014, 2024", "2016", "2008", "2009", "2022", "2025"
                ]
            }
            st.dataframe(pd.DataFrame(trophy_data), use_container_width=True)
        except Exception as e:
            logger.exception("Failed to display IPL overview.")
            st.error("An error occurred while loading the overview section.")

    def team_analysis(self, team):
        try:
            logger.info(f"Performing analysis for team: {team}")
            logo_path = f"image-video/{team.replace(' ', '_').lower()}.jpeg"
            col1, col2 = st.columns([1, 5])
            if os.path.exists(logo_path):
                col1.image(Image.open(logo_path), width=100)
            col2.header(f"{team} Analysis", divider='rainbow')

            players = list(self.ipl[self.ipl['BattingTeam'] == team]['batter'].unique())
            col1, col2 = st.columns([2, 1])
            selected_player = col1.selectbox("Select Player", players)
            img_path = get_image_path(selected_player)
            if img_path:
                col2.image(img_path, caption=selected_player, width=120)

            batter_df = self.ipl[self.ipl['batter'] == selected_player]
            batting_summary = (
                batter_df.groupby('BowlingTeam')
                .agg(Matches=('ID', 'nunique'), Runs=('batsman_run', 'sum'), Balls=('ballnumber', 'count'))
                .reset_index()
            )
            batting_summary['Strike Rate'] = (batting_summary['Runs'] / batting_summary['Balls']) * 100
            batting_summary['Run %'] = (batting_summary['Runs'] / batting_summary['Runs'].sum()) * 100

            st.subheader(f"📊 Batting Record of {selected_player}")
            st.dataframe(batting_summary, use_container_width=True)

            bowling_df = self.ipl[self.ipl['bowler'] == selected_player]
            if not bowling_df.empty:
                st.subheader(f"🎯 Bowling Record of {selected_player}")

                wicket_df = bowling_df[(bowling_df['isWicketDelivery'] == 1) & (bowling_df['player_out'].notna())]
                total_wickets = wicket_df.shape[0]
                total_balls = bowling_df.shape[0]
                total_overs = round(total_balls / 6, 1)
                total_runs = bowling_df['total_run'].sum()

                col1, col2, col3 = st.columns(3)
                col1.metric("Total Wickets", total_wickets)
                col2.metric("Total Overs", total_overs)
                col3.metric("Runs Conceded", total_runs)

                bowler_record = self.get_bowler_record(selected_player)
                st.dataframe(bowler_record, use_container_width=True)
            else:
                st.info(f"ℹ️ {selected_player} has not bowled in the IPL data.")

            if not batting_summary.empty:
                st.markdown(f"### 🥧 {selected_player} Run Contribution vs Each Team")
                fig, ax = plt.subplots()
                ax.pie(
                    batting_summary['Run %'],
                    labels=batting_summary['BowlingTeam'],
                    autopct='%1.1f%%',
                    startangle=90,
                    textprops={'fontsize': 8}
                )
                ax.axis('equal')
                st.pyplot(fig)
        except Exception as e:
            logger.exception(f"Error in team_analysis for {team}")
            st.error("Could not load team analysis. Please try another team.")

    def show_duel(self, batsman, bowler):
        try:
            logger.info(f"Showing duel: {batsman} vs {bowler}")
            duel_df = self.ipl[(self.ipl['batter'] == batsman) & (self.ipl['bowler'] == bowler)]
            if duel_df.empty:
                st.warning("❌ No data found for this player combination.")
                return

            runs = duel_df['batsman_run'].sum()
            balls = duel_df.shape[0]
            outs = duel_df[duel_df['player_out'] == batsman].shape[0]
            sr = (runs / balls * 100) if balls > 0 else 0

            st.subheader(f"🎯 {batsman} vs {bowler}")

            batsman_img = get_image_path(batsman)
            bowler_img = get_image_path(bowler)

            col1, col2 = st.columns(2)
            if batsman_img and os.path.exists(batsman_img):
                col1.image(batsman_img, caption=f"Batsman: {batsman}", width=200)
            if bowler_img and os.path.exists(bowler_img):
                col2.image(bowler_img, caption=f"Bowler: {bowler}", width=200)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Balls Faced", balls)
            col2.metric("Runs Scored", runs)
            col3.metric("Dismissals", outs)
            col4.metric("Strike Rate", round(sr, 2))

            plot_run_distribution(duel_df)
            plot_ball_timeline(duel_df)
        except Exception as e:
            logger.exception(f"Error showing duel between {batsman} and {bowler}")
            st.error("Failed to load player vs bowler data.")

    def run(self):
        try:
            logger.info("Running IPL dashboard main view.")
            st.sidebar.header(":green[IPL]-:red[Menu]", divider='rainbow')
            option = st.sidebar.selectbox(
                "Select Analysis",
                ['🏠-Overall IPL Analysis', '🧢-Team analysis', '⚔️-Player vs Bowler Duel',
                 '🏆-Leaderboard', "📊 Player Career Summary", "🏏-Team vs Team Analysis",
                 "📜-Tournament Summary", "📈-Player Comparison", "🏟️-Venue Insights", "🤖-Ask GenAI"]
            )

            if option == '🏠-Overall IPL Analysis':
                if st.sidebar.button("Show Overview"):
                    self.show_overview()

            elif option == '🧢-Team analysis':
                team = st.sidebar.selectbox("Select Team", sorted(self.ipl['BattingTeam'].unique()))
                self.team_analysis(team)

            elif option == '⚔️-Player vs Bowler Duel':
                batsman = st.sidebar.selectbox("Select Batsman", self.batsmen)
                bowler = st.sidebar.selectbox("Select Bowler", self.bowlers)
                if st.sidebar.button("\U0001F3AF Show Duel Record"):
                    self.show_duel(batsman, bowler)

            elif option == "🏆-Leaderboard":
                leaderboard_dashboard(self.ipl)

            elif option == "📊 Player Career Summary":
                player_summary_page(self.ipl)

            elif option == "🏏-Team vs Team Analysis":
                team_list = sorted(set(self.ipl['Team1'].unique()) | set(self.ipl['Team2'].unique()))
                team1 = st.sidebar.selectbox("Select Team 1", team_list)
                team2 = st.sidebar.selectbox("Select Team 2", [t for t in team_list if t != team1])
                if st.sidebar.button("Show Matchup Analysis"):
                    team_vs_team_analysis(self.ipl, team1, team2)

            elif option == '📜-Tournament Summary':
                tournament_summary_page()

            elif option == '📈-Player Comparison':
                player_detailed_comparison(self.ipl)

            elif option == "🏟️-Venue Insights":
                venue_analysis_page(self.ipl)

            elif option == "🤖-Ask GenAI":
                genai_chat_tab()
        except Exception as e:
            logger.exception("Error in dashboard run loop.")
            st.error("An error occurred while rendering the dashboard.")

