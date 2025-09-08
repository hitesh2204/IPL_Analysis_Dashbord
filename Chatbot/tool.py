from langchain.agents import tool
from src.functional_tools.player_summary_tool import get_player_summary
from src.functional_tools.team_vs_team_tool import get_team_vs_team_summary
from src.functional_tools.player_comparison_tool import get_player_comparison
from src.functional_tools.venue_analysis_tool import get_venue_summary
from src.functional_tools.tournament_summary_tool import get_tournament_summary
from src.functional_tools.leaderboard_tool import get_leaderboard_summary
from src.functional_tools.player_vs_team_tool import get_player_vs_team_summary
from src.functional_tools.phase_wise_tool import get_phase_wise_performance
from src.functional_tools.playoff_tool import get_playoff_performance
from src.functional_tools.pair_stats_tool import get_pair_stats
from src.functional_tools.rag_csv_tool import get_rag_tool
from src.utils import get_normalized_player_name  
from src.utils import normalize_venue_name
from src.utils import normalize_team_name  
from src.utils import extract_stat
import pandas as pd
from src.data_loader import load_ipl_data
from Chatbot.llm import load_llm 
import streamlit as st
import re

## importing llm model
llm = load_llm()
qa_chain = get_rag_tool(llm)

# Load IPL data globally
ipl = load_ipl_data()

# PLAYER TEXT SUMMARY TOOL
@tool
def get_player_summary_tool(player_name: str) -> str:
    """
    Returns a comprehensive IPL career summary for a given player.

    This includes key batting and bowling statistics such as total runs, 4s, 50s, Best Bowling,
    Dismissals, average, strike rate, Highest Score, Balls Faced, Total Wickets and other highlights.

    Input:
    - player_name (str): Full name or partial name of the IPL player (e.g., "Virat Kohli", "kohli", "VIRAT")

    Output:
    - A readable string summary containing batting and bowling stats.
    """

    # Normalize the player name
    all_players = ipl["batter"].unique().tolist()
    normalized_name = get_normalized_player_name(player_name, all_players)

    if not normalized_name:
        return f"Error: No close match found for '{player_name}'. Try a more accurate or complete name."


    # Call your existing summary function
    return get_player_summary(normalized_name)

# Team vs Team analysis.
@tool
def get_team_vs_team_summary_tool(query: str) -> str:
    """
    Provides a detailed head-to-head IPL summary between two teams.
    The summary includes:
    - Total matches played
    - Highest Team Score
    - Top 5 batsmen with most runs in these matchups
    - Top 5 bowlers with most wickets

    Input:
    - query (str): Must contain the names of **two IPL teams** in short code format (e.g., 'MI vs CSK', 'RCB vs KKR').

    Output:
    - A human-readable comparison of stats between the two teams.

    Example usage:
    "Show MI vs CSK summary".
    """
    teams = re.findall(r"(RCB|MI|CSK|RR|SRH|GT|LSG|KKR|PBKS|DC)", query, re.IGNORECASE)

    if len(teams) < 2:
        return "Error:Please provide two valid IPL teams in your query like 'Show MI vs CSK summary'."

    team1_raw, team2_raw = teams[0], teams[1]
    team1 = normalize_team_name(team1_raw)
    team2 = normalize_team_name(team2_raw)

    return get_team_vs_team_summary(team1, team2, ipl)


# 🧍‍♂️ PLAYER COMPARISON TOOL
@tool
def get_player_comparison_tool(player1: str, player2: str) -> str:
    """Compare batting and bowling performance of two IPL players.
    Accepts full or partial names, case-insensitive.
    """
    # Combine batter and bowler columns for full player list
    all_players = sorted(set(ipl["batter"].dropna().unique()) | set(ipl["bowler"].dropna().unique()))

    # Normalize both player names
    player1_normalized = get_normalized_player_name(player1, all_players)
    player2_normalized = get_normalized_player_name(player2, all_players)

    # Handle unmatched names
    if not player1_normalized:
        return f"Error:Could not find player matching '{player1}'"
    if not player2_normalized:
        return f"Error:Could not find player matching '{player2}'"

    # Handle duplicate normalized results
    if player1_normalized == player2_normalized:
        return f"Both inputs refer to the same player: {player1_normalized}"

    return get_player_comparison(player1_normalized, player2_normalized, ipl)


# VENUE ANALYSIS TOOL
@tool
def get_venue_summary_tool(venue_query: str) -> str:
    """Retrieve IPL match statistics for a specific venue.

    Input:
    - venue_query (str): Should include the name of the venue (e.g., "Wankhede Stadium", "Eden Gardens").

    Output:
    - A detailed summary of:
      • Total matches played
      • Total runs scored
      • Number of 4s and 6s hit
      • Top 5 batsmen by runs
      • Top 5 bowlers by wickets

    Example queries:
    - "Show stats at Wankhede Stadium"
    - "Eden Gardens IPL summary"

    This tool helps analyze venue-specific trends in IPL history.
    """
    return get_venue_summary(ipl, venue_query)

# TOURNAMENT OVERVIEW TOOL
@tool
def get_tournament_summary_tool(season_query: str) -> str:
    """Return a high-level summary of an IPL season or all seasons.
    Input:
    - season_query (str): Provide a specific season year (e.g., "2020", "2016") or "all" to get a summary across all seasons.

    Output includes:
    - Season winner
    - Final match results
    - Orange Cap and Purple Cap 
    - Total Matches

    Example queries:
    - "Show IPL 2020 summary"
    - "Give me IPL winners of all seasons"
    - "Summarize the 2016 IPL season"
    """
    return get_tournament_summary(season_query, ipl)

# LEADERBOARD TOOL
@tool
def get_leaderboard_summary_tool(query: str) -> str:
    """Return top-performing batsmen or bowlers in a specific IPL season or across all seasons.

    Input:
    - query (str): Must specify either "batsmen" or "bowlers" and optionally a season (e.g., "2020", "overall").

    Output:
    - Top 5 batsmen (based on total runs) or top 5 bowlers (based on wickets).
    - Season-specific or all-time leaderboard based on the query.

    Example queries:
    - "Top batsmen in IPL 2023"
    - "Show overall top bowlers"
    - "2020 leaderboard for batsmen"
    """
    return get_leaderboard_summary(query, ipl)


# Player vs Team Tool
@tool
def get_player_vs_team_tool(query: str) -> str:
    """
    Retrieve detailed performance statistics of a player against a specific IPL team, optionally filtered by season.

    Input Format:
    - "Player Name vs Team Name"
    - "Player Name vs Team Name in Season"

    Example Queries:
    - "Virat Kohli vs CSK"
    - "Rohit Sharma vs RCB in 2020"

    Output:
    - Batting and bowling stats of the player against the specified opponent.
    """
    match = re.match(r"(.+?)\s+vs\s+(.+?)(?:\s+in\s+(\d{4}))?$", query.strip(), re.IGNORECASE)
    if not match:
        return "Error:Invalid format. Use 'Player vs Team in Season' format."

    # Raw extracted names
    raw_player_name = match.group(1).strip()
    raw_team_name = match.group(2).strip()
    season = int(match.group(3)) if match.group(3) else None

    # Normalize player name
    all_players = set(ipl["batter"]).union(set(ipl["bowler"]))
    player_name = get_normalized_player_name(raw_player_name, all_players)
    if not player_name:
        return f"Error:Player '{raw_player_name}' not found in dataset."

    # Normalize team name
    team_name = normalize_team_name(raw_team_name)
    if not team_name:
        return f"Error: Team '{raw_team_name}' not recognized"

    return get_player_vs_team_summary(player_name, team_name, season, ipl)


# Phase Tool
@tool
def get_phase_wise_performance_tool(query: str) -> str:
    """
    Retrieve a player's batting and/or bowling performance during a specific phase of an IPL match.

    Accepted Phases:
    - Powerplay (Overs 1-6)
    - Middle Overs (Overs 7-15)
    - Death Overs (Overs 16-20)

    Input Formats:
    - "Player Name in Phase"
    - "Player Name in Phase in Season"

    Examples:
    - "Virat Kohli in Powerplay"
    - "MS Dhoni in Death Overs in 2021"

    Output:
    - Batting: Runs scored, strike rate, boundaries (4s, 6s)
    - Bowling (if applicable): Overs bowled, wickets, economy rate
    """
    match = re.match(r"(.+?)\s+in\s+([\w\s]+?)(?:\s+in\s+(\d{4}))?$", query.strip(), re.IGNORECASE)
    if not match:
        return "Error:Invalid format. Use: 'PlayerName in Phase [in Season]'"

    player_name = match.group(1).strip()
    phase = match.group(2).strip().lower()
    season = int(match.group(3)) if match.group(3) else None
    return get_phase_wise_performance(player_name, phase, season, ipl)

## playoff performance tools
@tool
def get_playoff_performance_tool(player_or_team_name: str) -> str:
    """Get the IPL Playoff performance of a specific player or team.

    Covers:
    - Qualifier 1
    - Eliminator
    - Qualifier 2
    - Final

    Input:
    - Player Name (e.g., "MS Dhoni")
    - Team Name (e.g., "Mumbai Indians")

    Output:
    - For players: Matches played, runs/wickets, SR/Economy, key performances
    - For teams: Matches played, wins/losses, win %, titles won

    Example:
    - "Virat Kohli"
    - "Chennai Super Kings"
    """
    all_players = ipl["batter"].unique().tolist()

    # Try player normalization first
    normalized_player = get_normalized_player_name(player_or_team_name, all_players)

    if normalized_player:
        return get_playoff_performance(normalized_player, ipl)

    # If not a player, try team normalization
    normalized_team = normalize_team_name(player_or_team_name)
    if normalized_team:
        return get_playoff_performance(normalized_team, ipl)

    return f"Error:'{player_or_team_name}' not found as a player or team in the dataset."

## Get pair stats tool
@tool
def get_pair_stats_tool(query: str) -> str:
    """
    Get partnership statistics between two players, optionally filtered by IPL season.

    Input Format:
    - "<Player1> and <Player2> in <Season>" (e.g., "Rohit Sharma and Virat Kohli in 2020")
    - Or just "<Player1> and <Player2>" for all seasons
    """
    try:
        # Regex to extract players & optional season
        pattern = r"(.+?)\s+and\s+(.+?)(?:\s+in\s+(\d{4}))?$"
        match = re.search(pattern, query.strip(), re.IGNORECASE)

        if not match:
            return "Error:Invalid format. Use: '<Player1> and <Player2> in <season>' or just '<Player1> and <Player2>'"

        raw_player1 = match.group(1).strip()
        raw_player2 = match.group(2).strip()
        season = match.group(3).strip() if match.group(3) else None

        # Prepare list of all unique player names
        player_names = sorted(set(ipl["batter"].unique().tolist() + ipl["non-striker"].unique().tolist()))

        # Normalize names
        player1 = get_normalized_player_name(raw_player1, player_names)
        player2 = get_normalized_player_name(raw_player2, player_names)

        return get_pair_stats(player1, player2, season)

    except Exception as e:
        return f"Error: fetching pair stats: {str(e)}"

## CSV-RAG tool
@tool
def get_rag_csv_tool(query: str) -> str:
    """
    Answer IPL-related natural language questions using a Retrieval-Augmented Generation (RAG) system.

    Uses a FAISS vector store built from IPL CSV data and a language model to retrieve and generate answers.

    Example queries:
    - "Who scored the most runs for RCB in 2016?"
    - "Which team won the most matches at Wankhede Stadium?"
    - "Top scorers against CSK in playoffs"
    - "Best bowling figures by Bumrah in 2020"
    """
    if not query or not query.strip():
        return "Error: Query cannot be empty."

    try:
        response = qa_chain.invoke({"query": query})
        result = response.get("result")
        return result if result else "Error: No answer found."
    except Exception as e:
        return f"Error: RAG system failed -> {str(e)}"


# ✅ Export all tools for agent
all_tools = [
    get_leaderboard_summary_tool,
    get_player_summary_tool,
    get_team_vs_team_summary_tool,
    get_player_comparison_tool,
    get_venue_summary_tool,
    get_tournament_summary_tool,
    get_powerplay_stats_tool,
    get_player_vs_team_tool,
    get_phase_wise_performance_tool,
    get_playoff_performance_tool,
    get_pair_stats_tool,
    get_rag_csv_tool
]