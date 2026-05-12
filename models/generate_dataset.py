"""
Antigravity - Addict Aware
Sample Dataset Generator for ML Training

Generates synthetic digital addiction data for training the Random Forest model.
"""
import pandas as pd
import numpy as np
import os

np.random.seed(42)

N_SAMPLES = 500


def generate_dataset():
    """Generate synthetic addiction assessment dataset"""
    data = []

    for _ in range(N_SAMPLES):
        # Randomly assign addiction category
        category = np.random.choice(['Low', 'Medium', 'High'], p=[0.3, 0.45, 0.25])

        if category == 'Low':
            screen_time = round(np.random.uniform(0.5, 3.5), 1)
            phone_pickups = int(np.random.randint(5, 40))
            social_media_time = round(np.random.uniform(0.2, 1.5), 1)

        elif category == 'Medium':
            screen_time = round(np.random.uniform(3.0, 7.0), 1)
            phone_pickups = int(np.random.randint(30, 80))
            social_media_time = round(np.random.uniform(1.5, 4.0), 1)

        else:  # High
            screen_time = round(np.random.uniform(6.0, 14.0), 1)
            phone_pickups = int(np.random.randint(60, 150))
            social_media_time = round(np.random.uniform(3.5, 8.0), 1)

        # Add some noise to make it realistic
        screen_time = max(0.1, screen_time + round(np.random.normal(0, 0.5), 1))
        phone_pickups = max(1, phone_pickups + int(np.random.normal(0, 5)))
        social_media_time = max(0.1, social_media_time + round(np.random.normal(0, 0.3), 1))

        data.append({
            'screen_time': screen_time,
            'phone_pickups': phone_pickups,
            'social_media_time': social_media_time,
            'addiction_level': category
        })

    df = pd.DataFrame(data)

    # Save to CSV
    dataset_path = os.path.join(os.path.dirname(__file__), 'addiction_dataset.csv')
    df.to_csv(dataset_path, index=False)
    print(f"[✓] Generated {N_SAMPLES} samples → {dataset_path}")
    print(f"    Distribution: {df['addiction_level'].value_counts().to_dict()}")

    return df


if __name__ == '__main__':
    generate_dataset()
