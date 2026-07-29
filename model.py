import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os

class MusicRecommender:
    def __init__(self, n_clusters=10, model_dir='models'):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.scaler = StandardScaler()
        self.model_dir = model_dir
        self.data = None
        
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

    def generate_synthetic_data(self, num_samples=5000):
        # Setting a seed for reproducible synthetic data
        np.random.seed(42)
        
        # Real-world-like distributions for track characteristics
        genres = ['Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Classical', 'Electronic', 'Country', 'R&B', 'Indie', 'Folk']
        
        data = {
            'id': [f'song_{i}' for i in range(num_samples)],
            'title': [f'Track {i}' for i in range(num_samples)],
            'artist': [f'Artist {i % 500}' for i in range(num_samples)],
            'genre': np.random.choice(genres, num_samples),
            # Audio features scaled realistically based on typical Spotify metrics
            'danceability': np.random.uniform(0.0, 1.0, num_samples),
            'energy': np.random.uniform(0.0, 1.0, num_samples),
            'key': np.random.randint(0, 12, num_samples),
            'loudness': np.random.uniform(-60.0, 0.0, num_samples),
            'mode': np.random.randint(0, 2, num_samples),
            'speechiness': np.random.uniform(0.0, 0.5, num_samples),
            'acousticness': np.random.uniform(0.0, 1.0, num_samples),
            'instrumentalness': np.random.uniform(0.0, 1.0, num_samples),
            'liveness': np.random.uniform(0.0, 1.0, num_samples),
            'valence': np.random.uniform(0.0, 1.0, num_samples),
            'tempo': np.random.uniform(60.0, 180.0, num_samples)
        }
        self.data = pd.DataFrame(data)
        return self.data

    def get_feature_columns(self):
        return ['danceability', 'energy', 'key', 'loudness', 'mode', 
                'speechiness', 'acousticness', 'instrumentalness', 
                'liveness', 'valence', 'tempo']

    def train(self):
        if self.data is None:
            raise ValueError("No data available. Call generate_synthetic_data() first.")
        
        features = self.data[self.get_feature_columns()]
        
        # Standardize features for KMeans and Cosine Similarity
        scaled_features = self.scaler.fit_transform(features)
        
        # Partition data into clusters
        self.data['cluster'] = self.kmeans.fit_predict(scaled_features)
        
        # Persist the models and clustered dataset for rapid API access
        joblib.dump(self.kmeans, f'{self.model_dir}/kmeans_model.pkl')
        joblib.dump(self.scaler, f'{self.model_dir}/scaler.pkl')
        self.data.to_csv(f'{self.model_dir}/song_data_clustered.csv', index=False)
        
        print(f"Model trained and {len(self.data)} records saved successfully.")

    def load_model(self):
        try:
            # We don't actually persist the K-Means object to memory once clustered, 
            # as our cosine similarity only needs the data and the scaler,
            # but we load anyway to ensure structural integrity.
            self.kmeans = joblib.load(f'{self.model_dir}/kmeans_model.pkl')
            self.scaler = joblib.load(f'{self.model_dir}/scaler.pkl')
            self.data = pd.read_csv(f'{self.model_dir}/song_data_clustered.csv')
            return True
        except FileNotFoundError:
            return False

    def recommend(self, song_title, top_k=5, mood=None):
        if self.data is None:
            success = self.load_model()
            if not success:
                raise ValueError("System not trained. Awaiting dataset processing.")
                
        # Locate the requested track
        song_idx = self.data[self.data['title'].str.lower() == song_title.lower()].index
        if len(song_idx) == 0:
            return {"error": "Song not found in the dataset.", "recommendations": []}
        
        song_idx = song_idx[0]
        song_cluster = self.data.loc[song_idx, 'cluster']
        
        # Optimization: Only compare against tracks in the same K-Means cluster
        cluster_songs = self.data[self.data['cluster'] == song_cluster].copy()
        
        # We need the index of the target song within the cluster
        features = cluster_songs[self.get_feature_columns()]
        scaled_features = self.scaler.transform(features)
        
        target_features = self.scaler.transform(self.data.loc[[song_idx]][self.get_feature_columns()])
        
        # Compute Cosine Similarities natively handling multidimensional vectors
        similarities = cosine_similarity(target_features, scaled_features)[0]
        cluster_songs['similarity'] = similarities
        
        # Exclude the exact target song from recommendations
        recommendations = cluster_songs[cluster_songs['id'] != self.data.loc[song_idx, 'id']]
        
        if mood:
            mood = mood.lower()
            filtered = recommendations.copy()
            if mood == 'happy':
                filtered = recommendations[(recommendations['valence'] > 0.5) & (recommendations['energy'] > 0.5)]
            elif mood == 'sad':
                filtered = recommendations[(recommendations['valence'] < 0.4)]
            elif mood == 'energetic':
                filtered = recommendations[recommendations['energy'] > 0.7]
            elif mood == 'chill':
                filtered = recommendations[(recommendations['energy'] < 0.5) & (recommendations['acousticness'] > 0.5)]
            
            # fallback to unfiltered if filtering leaves fewer than top_k items
            if len(filtered) >= top_k:
                recommendations = filtered
                
        # Retrieve the closest logical matches
        recommendations = recommendations.sort_values(by='similarity', ascending=False).head(top_k)
        
        results = []
        for _, row in recommendations.iterrows():
            results.append({
                "title": row['title'],
                "artist": row['artist'],
                "genre": row['genre'],
                "similarity": round(row['similarity'] * 100, 2), # Convert to percentage
                "features": {
                    "danceability": round(row['danceability'], 2),
                    "energy": round(row['energy'], 2),
                    "valence": round(row['valence'], 2)
                }
            })
            
        target_info = {
            "title": self.data.loc[song_idx, 'title'], 
            "artist": self.data.loc[song_idx, 'artist'],
            "genre": self.data.loc[song_idx, 'genre']
        }
        return {"recommendations": results, "target": target_info}

if __name__ == "__main__":
    recommender = MusicRecommender()
    print("Generating synthetic 5000-track dataset...")
    recommender.generate_synthetic_data(5000)
    print("Executing K-Means Clustering and saving models...")
    recommender.train()
    
    print("\n--- Diagnostic Check: Recommending alternatives to 'Track 404' ---")
    recommendations = recommender.recommend("Track 404")
    if "error" not in recommendations:
        for rec in recommendations['recommendations']:
            print(f"- {rec['title']} by {rec['artist']} ({rec['genre']}) => {rec['similarity']}% match")
    else:
        print(recommendations['error'])
