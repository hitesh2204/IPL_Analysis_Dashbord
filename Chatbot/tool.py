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
from src.functional_tools.rag_csv_tool import get_rag_tool
import pandas as pd
from src.data_loader import load_ipl_data
import streamlit as st
import re

# Load IPL data globally
ipl = load_ipl_data()

# 📊 PLAYER TEXT SUMMARY TOOL
@tool
def get_player_summary_tool(player_name: str) -> str:
    """
    Returns a comprehensive IPL career summary for a given player.

    This includes key batting and bowling statistics such as total runs,4s,50s,Best Bowling,
    Dismissals,average,strike rate,Highest Score,Balls Faced,Total Wickets and other highlights.
    
    Input:
    - player_name (str): Full name of the IPL player (e.g., "Virat Kohli")

    Output:
    - A readable string summary containing batting and bowling stats.
    """
    return get_player_summary(player_name)


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
    import re
    teams = re.findall(r"(RCB|MI|CSK|RR|SRH|GT|LSG|KKR|PBKS|DC)", query, re.IGNORECASE)

    if len(teams) < 2:
        return "Please provide two valid IPL teams in your query like 'Show MI vs CSK summary'."

    team1, team2 = teams[0].upper(), teams[1].upper()
    return get_team_vs_team_summary(team1, team2, ipl)

# 🧍‍♂️ PLAYER COMPARISON TOOL
@tool
def get_player_comparison_tool(player_query: str) -> str:
    """Compare batting and bowling performance of two or more IPL players.

    Input:
    - player_query (str): Should contain player names separated by commas or 'vs'.
      Example: "Virat Kohli vs Rohit Sharma" or "Dhoni, Raina, AB de Villiers"

    Output:
    - A detailed comparison of IPL stats (runs,4s,wickets,averages,strike rates,etc.)
      for each mentioned player.

    This tool helps answer queries like:
    - "Compare Kohli vs Rohit"
    - "Show stats of Raina, Dhoni, and ABD"
    """
    return get_player_comparison(player_query,ipl)

# 🏟️ VENUE ANALYSIS TOOL
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

# 🧾 TOURNAMENT OVERVIEW TOOL
@tool
def get_tournament_summary_tool(season_query: str) -> str:
    """Return a high-level summary of an IPL season or all seasons.
    Input:
    - season_query (str): Provide a specific season year (e.g., "2020", "2016") or "all" to get a summary across all seasons.

    Output includes:
    - Season winner
    - Final match result
    - Orange Cap and Purple Cap 
    - Total Matches

    Example queries:
    - "Show IPL 2020 summary"
    - "Give me IPL winners of all seasons"
    - "Summarize the 2016 IPL season"
    """
    return get_tournament_summary(season_query, ipl)

# 🏆 LEADERBOARD TOOL
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

# 🔋 POWERPLAY TOOL
@tool
def get_powerplay_summary_tool(query: str) -> str:
    """Return the Powerplay performance summary of an IPL team for a specific season or overall.

    Input:
    - A string containing the team name, optionally followed by a season year.
      Format: "Team Name, Season" (e.g., "MI, 2020") or just "Team Name" (e.g., "CSK").

    Output:
    - Statistics of Powerplay overs (0-6) for the team including total runs, wickets lost, Strike Rate, etc.
    - If no season is provided, returns overall Powerplay performance.

    Example queries:
    - "RCB, 2023"
    - "RR"
    """
    return get_powerplay_summary(query,ipl)

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
    - Batting and bowling stats of the player against the specified opponent, including total runs, strike rate, dismissals, average, Balls Faced, and wickets (if applicable).
    - If a season is provided, results are scoped to that season; otherwise, career stats are shown.
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
    trieve a player's batting and/or bowling performance during a specific phase of an IPL match.

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
        return "❌ Invalid format. Use: 'PlayerName in Phase [in Season]'"

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
    return get_playoff_performance(player_or_team_name, ipl)

# 👬 PAIR STATS TOOL
@tool
def get_pair_stats_tool(query: str) -> str:
    """Get partnership statistics between two players, optionally filtered by IPL season.

    Input Format:
    - "<Player1> and <Player2> in <Season>" (e.g., "Rohit Sharma and Virat Kohli in 2020")
    - Or just "<Player1> and <Player2>" for all seasons

    Output:
    - Matches Played Together
    - Total runs scored together
    - Average partnership
    - Balls Faced Together
    - (Optional) Season-specific breakdown

    Example:
    - "AB de Villiers and Virat Kohli in 2016"
    - "David Warner and Jonny Bairstow"
    """
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
    

## CSV-RAG tool
@tool
def get_rag_csv_tool(query: str) -> str:
    """Answer IPL-related natural language questions using a Retrieval-Augmented Generation (RAG) system.

    This tool uses a FAISS vector store built from IPL CSV data and a language model to retrieve and generate answers.

     How it works:
    - Embeds the IPL dataset into a FAISS vector store
    - Uses the query to retrieve relevant chunks
    - Passes them to an LLM to generate a contextual answer

     Example queries:
    - "Who scored the most runs for RCB in 2016?"
    - "Which team won the most matches at Wankhede Stadium?"
    - "Top scorers against CSK in playoffs"
    - "Best bowling figures by Bumrah in 2020"
    """
    qa_chain = get_rag_tool()
    return qa_chain.run(query)


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
    get_pair_stats_tool,
    get_rag_csv_tool
]