"""
Antigravity - Addict Aware
Convert Kaggle Mobile Usage ScreenTime Dataset to project format.

Maps Kaggle columns to existing features (screen_time, phone_pickups, social_media_time)
and derives addiction_level (Low / Medium / High) using KMeans clustering.
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# Paths
SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
KAGGLE_FILE = os.path.join(PROJECT_ROOT, 'Mobile_Usage_Screentime_Dataset_.xlsx')
OUTPUT_CSV = os.path.join(SCRIPT_DIR, 'addiction_dataset.csv')

FEATURES = ['screen_time', 'phone_pickups', 'social_media_time']


def convert_kaggle_dataset():
    """
    Convert the Kaggle Mobile Usage ScreenTime Dataset to project format.

    Column Mapping:
        Daily_ScreenTime_Hours  → screen_time       (direct, hours/day)
        Messages_Sent           → phone_pickups      (proxy for phone engagement)
        SocialMedia_Min / 60    → social_media_time   (convert minutes → hours)

    Addiction Level Derivation:
        KMeans clustering (3 clusters) on standardized features,
        mapped to Low/Medium/High by average screen time per cluster.
    """
    # Read Kaggle dataset
    if not os.path.exists(KAGGLE_FILE):
        raise FileNotFoundError(
            f"Kaggle dataset not found at: {KAGGLE_FILE}\n"
            "Please download it from https://www.kaggle.com/datasets/youssmanaveed/mobile-usage-screentime-dataset"
        )

    raw_df = pd.read_excel(KAGGLE_FILE)
    print(f"[i] Loaded Kaggle dataset: {raw_df.shape[0]} rows, {raw_df.shape[1]} columns")

    # === Map columns ===
    converted = pd.DataFrame()
    converted['screen_time'] = raw_df['Daily_ScreenTime_Hours'].round(1)
    converted['phone_pickups'] = raw_df['Messages_Sent'].astype(int)
    converted['social_media_time'] = (raw_df['SocialMedia_Min'] / 60).round(1)

    # === Derive addiction_level using KMeans clustering ===
    # Standardize features for better clustering
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(converted[FEATURES].values)

    # Find 3 natural clusters in the data
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    # Map cluster IDs to Low/Medium/High based on average screen time
    cluster_means = {}
    for c in range(3):
        cluster_means[c] = converted.loc[clusters == c, 'screen_time'].mean()

    sorted_clusters = sorted(cluster_means, key=cluster_means.get)
    label_map = {
        sorted_clusters[0]: 'Low',
        sorted_clusters[1]: 'Medium',
        sorted_clusters[2]: 'High'
    }
    converted['addiction_level'] = [label_map[c] for c in clusters]

    # === Data Augmentation: 5x per sample with noise ===
    print("[i] Augmenting dataset (5x per sample)...")
    aug_rows = []
    np.random.seed(42)
    for _, row in converted.iterrows():
        aug_rows.append(row.to_dict())  # keep original
        for _ in range(5):
            noisy = {
                'screen_time': round(max(0.1, row['screen_time'] + np.random.normal(0, 0.1) * row['screen_time']), 1),
                'phone_pickups': max(1, int(row['phone_pickups'] + np.random.normal(0, 0.1) * row['phone_pickups'])),
                'social_media_time': round(max(0.1, row['social_media_time'] + np.random.normal(0, 0.1) * row['social_media_time']), 1),
                'addiction_level': row['addiction_level']
            }
            aug_rows.append(noisy)

    augmented_df = pd.DataFrame(aug_rows)

    # Save to CSV
    augmented_df.to_csv(OUTPUT_CSV, index=False)

    # Print summary
    dist = augmented_df['addiction_level'].value_counts()
    print(f"[✓] Converted + augmented dataset saved → {OUTPUT_CSV}")
    print(f"    Original: {len(converted)} rows → Augmented: {len(augmented_df)} rows")
    print(f"    Distribution: Low={dist.get('Low', 0)}, Medium={dist.get('Medium', 0)}, High={dist.get('High', 0)}")
    print(f"\n    Feature ranges:")
    print(f"      screen_time:       {augmented_df['screen_time'].min()} - {augmented_df['screen_time'].max()} hours")
    print(f"      phone_pickups:     {augmented_df['phone_pickups'].min()} - {augmented_df['phone_pickups'].max()}")
    print(f"      social_media_time: {augmented_df['social_media_time'].min()} - {augmented_df['social_media_time'].max()} hours")

    return augmented_df


if __name__ == '__main__':
    convert_kaggle_dataset()
