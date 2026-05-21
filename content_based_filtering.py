import joblib
import numpy as np
import pandas as pd
from scipy.sparse import save_npz
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler

from data_cleaning import data_for_content_filtering


CLEANED_DATA_PATH = "data/cleaned_data.csv"

ohe_cols = ["artist", "time_signature", "key"]
tfidf_col = "tags"
standard_scale_cols = ["year", "duration_ms", "loudness", "tempo"]
min_max_scale_cols = [
    "danceability",
    "energy",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
]


def train_transformer(data):
    """
    Train and persist the content-based preprocessing pipeline.
    """
    transformer = ColumnTransformer(
        transformers=[
            ("ohe", OneHotEncoder(handle_unknown="ignore"), ohe_cols),
            ("tfidf", TfidfVectorizer(max_features=85), tfidf_col),
            ("standard_scale", StandardScaler(), standard_scale_cols),
            ("min_max_scale", MinMaxScaler(), min_max_scale_cols),
        ],
        remainder="passthrough",
        n_jobs=1,
    )
    transformer.fit(data)
    joblib.dump(transformer, "transformer.joblib")


def transform_data(data):
    """
    Transform the input data using the persisted transformer.
    """
    transformer = joblib.load("transformer.joblib")
    return transformer.transform(data)


def save_transformed_data(transformed_data, save_path):
    """
    Save a sparse matrix to disk.
    """
    save_npz(save_path, transformed_data)


def calculate_similarity_scores(input_vector, data):
    """
    Calculate cosine similarity scores for the provided vector against the dataset.
    """
    return cosine_similarity(input_vector, data)


def content_recommendation(song_name, artist_name, songs_data, transformed_data, k=10):
    """
    Recommend the top k similar songs using content-based filtering.
    """
    song_name = song_name.lower()
    artist_name = artist_name.lower()

    song_row = songs_data.loc[(songs_data["name"] == song_name) & (songs_data["artist"] == artist_name)]
    song_index = song_row.index[0]
    input_vector = transformed_data[song_index].reshape(1, -1)
    similarity_scores = calculate_similarity_scores(input_vector, transformed_data)
    top_k_songs_indexes = np.argsort(similarity_scores.ravel())[-k - 1 :][::-1]
    top_k_songs_names = songs_data.iloc[top_k_songs_indexes]
    return top_k_songs_names[["name", "artist", "spotify_preview_url"]].reset_index(drop=True)


def main(data_path):
    """
    Train the preprocessing pipeline and persist the transformed content features.
    """
    data = pd.read_csv(data_path)
    data_content_filtering = data_for_content_filtering(data)
    train_transformer(data_content_filtering)
    transformed_data = transform_data(data_content_filtering)
    save_transformed_data(transformed_data, "data/transformed_data.npz")


if __name__ == "__main__":
    main(CLEANED_DATA_PATH)
