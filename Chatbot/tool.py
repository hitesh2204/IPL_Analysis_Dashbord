from langchain.agents import tool
from src.player_summary import get_player_summary
from src.team_vs_team import get_team_vs_team_summary
from src.player_comparison import get_player_comparison
from src.venue_analysis import get_venue_summary
from src.tournament_summary import get_tournament_summary
from src.leaderboard import get_leaderboard_summary
import pandas as pd
import streamlit as st
import re

# Load IPL data globally
ipl = pd.read_csv("IPL_Dataset//final_ipl.csv")

# 📊 PLAYER TEXT SUMMARY TOOL
@tool
def get_player_summary_tool(player_name: str) -> str:
    """Get IPL batting and bowling summary of a player by name."""
    return get_player_summary(player_name)

# Team vs Team analysis.
@tool
def get_team_vs_team_summary_tool(query: str) -> str:
    """
    Return head-to-head summary, top 5 batsmen and bowlers between two IPL teams.
    Input must contain both team names like 'MI vs CSK'.
    """
    import re
    teams = re.findall(r"(RCB|MI|CSK|RR|SRH|GT|LSG|KKR|PBKS|DC)", query, re.IGNORECASE)

    if len(teams) < 2:
        return "Please provide two valid IPL teams in your query like 'Show MI vs CSK summary'."

    team1, team2 = teams[0].upper(), teams[1].upper()
    return get_team_vs_team_summary(team1, team2, ipl)

# 🧍‍♂️ PLAYER COMPARISON TOOL
@tool
def get_player_comparison_tool(player_query: str) -> str:
    """Compare IPL stats for two or more players. Input should be player names separated by commas or 'vs'."""
    return get_player_comparison(player_query,ipl)

# 🏟️ VENUE ANALYSIS TOOL
@tool
def get_venue_summary_tool(venue_query: str) -> str:
    """Get summary of IPL stats at a specific venue, including top 5 batsmen, top 5 bowlers, total runs, 4s, and 6s."""
    return get_venue_summary(ipl, venue_query)

# 🧾 TOURNAMENT OVERVIEW TOOL
@tool
def get_tournament_summary_tool(season_query: str) -> str:
    """Provide a high-level summary of a specific IPL season."""
    return get_tournament_summary(season_query, ipl)

# 🏆 LEADERBOARD TOOL
@tool
def get_leaderboard_summary_tool(query: str) -> str:
    """Show top batsmen or bowlers in a season or overall IPL history."""
    return get_leaderboard_summary(query, ipl)


# ✅ Export all tools for agent
all_tools = [
    get_leaderboard_summary_tool,
    get_player_summary_tool,
    get_team_vs_team_summary_tool,
    get_player_comparison_tool,
    get_venue_summary_tool,
    get_tournament_summary_tool
]