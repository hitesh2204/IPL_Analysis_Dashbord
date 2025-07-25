from langchain.agents import tool
from src.utils import normalize_team_name  # for safe use
from src.functional_tools.player_summary_tool import get_player_summary
from src.functional_tools.team_vs_team_tool import get_team_vs_team_summary
from src.functional_tools.player_comparison_tool import get_player_comparison
from src.functional_tools.venue_analysis_tool import get_venue_summary
from src.functional_tools.tournament_summary_tool import get_tournament_summary
from src.functional_tools.leaderboard_tool import get_leaderboard_summary
from src.functional_tools.powerplay_tool import get_powerplay_summary
from src.functional_tools.player_vs_team_tool import get_player_vs_team_summary
from src.functional_tools.phase_wise_tool import get_phase_wise_performance
from src.functional_tools.playoff_tool import get_playoff_performance
from src.functional_tools.pair_stats_tool import get_pair_stats
import pandas as pd
from src.data_loader import load_ipl_data
import streamlit as st
import re

# Load IPL data globally
ipl = load_ipl_data()

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

# 🔋 POWERPLAY TOOL
@tool
def get_powerplay_summary_tool(query: str) -> str:
    """Get Powerplay performance summary for a team and season. Input format: 'Team Name, Season' or just 'Team Name'."""
    return get_powerplay_summary(query,ipl)

# Player vs Team Tool
@tool
def get_player_vs_team_tool(query: str) -> str:
    """
    Show performance of a player against a specific team. 
    Query format: "player_name vs team_name in season" or just "player_name vs team_name"
    Example: "Virat Kohli vs CSK in 2021"
    """
    match = re.match(r"(.+?)\s+vs\s+(.+?)(?:\s+in\s+(\d{4}))?$", query.strip(), re.IGNORECASE)
    if not match:
        return "Invalid format. Use 'Player vs Team in Season' format."

    player_name = match.group(1).strip()
    team_name = normalize_team_name(match.group(2).strip())
    season = int(match.group(3)) if match.group(3) else None

    return get_player_vs_team_summary(player_name, team_name, season, ipl)

# Phase Tool
@tool
def get_phase_wise_performance_tool(query: str) -> str:
    """
    Get a player's performance in a specific phase: Powerplay, Middle Overs, or Death Overs.
    Input format: "PlayerName in Phase [in Season]"
    Example: "Virat Kohli in Powerplay in 2020"
    """
    match = re.match(r"(.+?)\s+in\s+([\w\s]+?)(?:\s+in\s+(\d{4}))?$", query.strip(), re.IGNORECASE)
    if not match:
        return "❌ Invalid format. Use: 'PlayerName in Phase [in Season]'"

    player_name = match.group(1).strip()
    phase = match.group(2).strip().lower()
    season = int(match.group(3)) if match.group(3) else None
    return get_phase_wise_performance(player_name, phase, season, ipl)

@tool
def get_playoff_performance_tool(player_or_team_name: str) -> str:
    """Get a player's or team's performance in IPL Playoff matches (Qualifier, Eliminator, Final)."""
    return get_playoff_performance(player_or_team_name, ipl)

# 👬 PAIR STATS TOOL
@tool
def get_pair_stats_tool(query: str) -> str:
    """Get partnership stats between two players optionally filtered by season."""
    try:
        import re
        # Example query: "Stats of Rohit Sharma and Virat Kohli in 2020"
        pattern = r"(.*?)\s+and\s+(.*?)\s+(?:in\s+(\d{4}))?"
        match = re.search(pattern, query, re.IGNORECASE)

        if not match:
            return "Invalid format. Use: '<Player1> and <Player2> in <season>' or without season."

        player1 = match.group(1).strip()
        player2 = match.group(2).strip()
        season = match.group(3).strip() if match.group(3) else None

        return get_pair_stats(player1, player2, season)

    except Exception as e:
        return f"❌ Error in get_pair_stats_tool: {str(e)}"


# ✅ Export all tools for agent
all_tools = [
    get_leaderboard_summary_tool,
    get_player_summary_tool,
    get_team_vs_team_summary_tool,
    get_player_comparison_tool,
    get_venue_summary_tool,
    get_tournament_summary_tool,
    get_powerplay_summary_tool,
    get_player_vs_team_tool,
    get_phase_wise_performance_tool,
    get_playoff_performance_tool,
    get_pair_stats_tool
]