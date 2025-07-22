import pandas as pd

def generate_team_records_csv(ipl):
    match_results = []

    # Only keep unique match-level rows for win records
    match_df = ipl.drop_duplicates(subset='ID')

    # Teams that have played in either Team1 or Team2
    teams = sorted(set(match_df['Team1'].unique()) | set(match_df['Team2'].unique()))

    for team in teams:
        team_matches = match_df[(match_df['Team1'] == team) | (match_df['Team2'] == team)]
        total_matches = team_matches.shape[0]

        wins = team_matches[team_matches['WinningTeam'] == team].shape[0]
        losses = team_matches[
            (team_matches['WinningTeam'].notnull()) &
            (team_matches['WinningTeam'] != team) &
            ((team_matches['Team1'] == team) | (team_matches['Team2'] == team))
        ].shape[0]

        no_results = total_matches - (wins + losses)
        win_pct = round((wins / total_matches) * 100, 2) if total_matches > 0 else 0.0

        match_results.append({
            'team': team,
            'matches_played': total_matches,
            'wins': wins,
            'losses': losses,
            'no_results': no_results,
            'win_percentage': win_pct
        })

    df = pd.DataFrame(match_results)
    df.to_csv("ipl_dataset//rag_knowledgebase//team_records.csv", index=False)
    print("✅ team_records.csv generated successfully!")

# Run the function with your IPL DataFrame
if __name__ == "__main__":
    ipl = pd.read_csv("ipl_dataset//ipl_df.csv")
    generate_team_records_csv(ipl)
