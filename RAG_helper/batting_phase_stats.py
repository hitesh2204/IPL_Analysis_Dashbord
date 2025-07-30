import pandas as pd
import os

def generate_batting_phase_stats(input_csv_path, output_folder):
    # Load data
    df = pd.read_csv(input_csv_path,encoding='ISO-8859-1')

    # ✅ Sanity check for required columns
    required_cols = ['ID', 'Season', 'BattingTeam', 'batter', 'overs', 'ballnumber', 'batsman_run', 'total_run']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # ✅ Add phase based on over
    def get_phase(over):
        if 1 <= over <= 6:
            return 'Powerplay'
        elif 7 <= over <= 15:
            return 'Middle Overs'
        else:
            return 'Death Overs'

    df['phase'] = df['overs'].apply(get_phase)

    # ✅ Calculate 4s and 6s
    df['is_four'] = df['batsman_run'].apply(lambda x: 1 if x == 4 else 0)
    df['is_six'] = df['batsman_run'].apply(lambda x: 1 if x == 6 else 0)

    # ✅ Group by batter, team, phase
    phase_stats = df.groupby(['batter', 'BattingTeam', 'phase']).agg(
        matches=('ID', lambda x: x.nunique()),
        innings=('ID', lambda x: x.nunique()),  # unique matches played in phase
        runs=('batsman_run', 'sum'),
        balls_faced=('ballnumber', 'count'),  # Assuming ball-level data
        fours=('is_four', 'sum'),
        sixes=('is_six', 'sum')
    ).reset_index()

    # ✅ Calculate strike rate
    phase_stats['strike_rate'] = (phase_stats['runs'] / phase_stats['balls_faced'] * 100).round(2)

    # ✅ Rename columns for clarity
    phase_stats.rename(columns={
        'BattingTeam': 'team',
    }, inplace=True, errors='ignore')

    # ✅ Cast to int for readability
    phase_stats[['matches', 'innings']] = phase_stats[['matches', 'innings']].astype(int)

    # ✅ Reorder columns
    phase_stats = phase_stats[[
        'batter', 'team', 'phase', 'matches', 'innings', 'runs', 'balls_faced', 'strike_rate', 'fours', 'sixes'
    ]]

    # ✅ Save as CSV
    os.makedirs(output_folder, exist_ok=True)
    phase_stats.to_csv(os.path.join(output_folder, 'batting_phase_stats1.csv'), index=False)
    print("✅ batting_phase_stats.csv generated successfully.")

if __name__ == "__main__":
    generate_batting_phase_stats("IPL_Dataset/final_ipl.csv", "ipl_dataset/rag_knowledgebase")
