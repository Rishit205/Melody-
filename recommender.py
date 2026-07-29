import pandas as pd
import joblib
import os

from sklearn.metrics.pairwise import cosine_similarity


# =========================
# BASE DIRECTORY
# =========================
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# =========================
# FILE PATHS
# =========================
DATASET_PATH = os.path.join(
    BASE_DIR,
    "song_dataset_clustered.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "optimised_model.joblib"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "scaler.joblib"
)


# =========================
# LOAD DATASET
# =========================
df = pd.read_csv(DATASET_PATH)


# =========================
# LOAD MODEL + SCALER
# =========================
kmeans = joblib.load(MODEL_PATH)

scaler = joblib.load(SCALER_PATH)


# =========================
# PREPROCESSING
# =========================
df = df.drop_duplicates(
    subset=["name", "artist"]
)

df = df.dropna()

df["name_lower"] = (
    df["name"]
    .astype(str)
    .str.lower()
    .str.strip()
)


# =========================
# FEATURES
# =========================
features = [

    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "liveness",
    "valence",
    "tempo",
    "key",
    "mode",
    "time_signature"
]


X = df[features]

X_scaled = scaler.transform(X)


# =========================
# RECOMMEND FUNCTION
# =========================
def recommend(song_name, n=10):

    song_name = (
        song_name
        .lower()
        .strip()
    )

    # SONG NOT FOUND
    if song_name not in df["name_lower"].values:

        return []


    # GET SONG INDEX
    idx = df[
        df["name_lower"] == song_name
    ].index[0]


    # GET CLUSTER
    cluster = df.iloc[idx]["cluster"]


    # FILTER SAME CLUSTER
    cluster_df = df[
        df["cluster"] == cluster
    ]


    cluster_indices = cluster_df.index


    # GET CLUSTER VECTORS
    cluster_vectors = X_scaled[
        cluster_indices
    ]


    # TARGET SONG VECTOR
    song_vector = X_scaled[idx].reshape(1, -1)


    # COSINE SIMILARITY
    scores = cosine_similarity(
        song_vector,
        cluster_vectors
    )[0]


    # ZIP SCORES
    scores = list(
        zip(cluster_indices, scores)
    )


    # SORT DESCENDING
    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )


    recommendations = []


    # SKIP FIRST SONG
    for i in scores[1:n+1]:

        row = df.iloc[i[0]]

        recommendations.append({

            "name": row["name"],

            "artist": row["artist"],

            "cluster": int(row["cluster"]),

            "similarity": round(
                float(i[1]),
                3
            )
        })


    return recommendations