from pathlib import Path

import pandas as pd
import streamlit as st
from numpy import load
from scipy.sparse import load_npz

from content_based_filtering import content_recommendation
from hybrid_recommendations import HybridRecommenderSystem
from local_data import ensure_local_artifacts


PROJECT_ROOT = Path(__file__).resolve().parent


@st.cache_resource(show_spinner=False)
def load_app_assets():
    ensure_local_artifacts()

    return {
        "songs_data": pd.read_csv(PROJECT_ROOT / "data" / "cleaned_data.csv"),
        "transformed_data": load_npz(PROJECT_ROOT / "data" / "transformed_data.npz"),
        "track_ids": load(PROJECT_ROOT / "data" / "track_ids.npy", allow_pickle=True),
        "filtered_data": pd.read_csv(PROJECT_ROOT / "data" / "collab_filtered_data.csv"),
        "interaction_matrix": load_npz(PROJECT_ROOT / "data" / "interaction_matrix.npz"),
        "transformed_hybrid_data": load_npz(PROJECT_ROOT / "data" / "transformed_hybrid_data.npz"),
    }


with st.spinner("Preparing local data for the first run. This can take a few minutes."):
    try:
        assets = load_app_assets()
    except Exception as exc:
        st.error(f"Unable to start the app locally: {exc}")
        st.stop()


songs_data = assets["songs_data"]
transformed_data = assets["transformed_data"]
track_ids = assets["track_ids"]
filtered_data = assets["filtered_data"]
interaction_matrix = assets["interaction_matrix"]
transformed_hybrid_data = assets["transformed_hybrid_data"]


st.title("Welcome to the Spotify Song Recommender!")
st.write("### Enter the name of a song and the recommender will suggest similar songs")

song_name = st.text_input("Enter a song name:")
st.write("You entered:", song_name)

artist_name = st.text_input("Enter the artist name:")
st.write("You entered:", artist_name)

song_name = song_name.lower()
artist_name = artist_name.lower()

k = st.selectbox("How many recommendations do you want?", [5, 10, 15, 20], index=1)

if ((filtered_data["name"] == song_name) & (filtered_data["artist"] == artist_name)).any():
    filtering_type = "Hybrid Recommender System"
    diversity = st.slider(
        label="Diversity in Recommendations",
        min_value=1,
        max_value=9,
        value=5,
        step=1,
    )
    content_based_weight = 1 - (diversity / 10)
    chart_data = pd.DataFrame(
        {
            "type": ["Personalized", "Diverse"],
            "ratio": [10 - diversity, diversity],
        }
    )
    st.bar_chart(chart_data, x="type", y="ratio")
else:
    filtering_type = "Content-Based Filtering"


if filtering_type == "Content-Based Filtering":
    if st.button("Get Recommendations"):
        if ((songs_data["name"] == song_name) & (songs_data["artist"] == artist_name)).any():
            st.write("Recommendations for", f"**{song_name}** by **{artist_name}**")
            recommendations = content_recommendation(
                song_name=song_name,
                artist_name=artist_name,
                songs_data=songs_data,
                transformed_data=transformed_data,
                k=k,
            )

            for ind, recommendation in recommendations.iterrows():
                recommendation_name = recommendation["name"].title()
                recommendation_artist = recommendation["artist"].title()

                if ind == 0:
                    st.markdown("## Currently Playing")
                    st.markdown(f"#### **{recommendation_name}** by **{recommendation_artist}**")
                elif ind == 1:
                    st.markdown("### Next Up")
                    st.markdown(f"#### {ind}. **{recommendation_name}** by **{recommendation_artist}**")
                else:
                    st.markdown(f"#### {ind}. **{recommendation_name}** by **{recommendation_artist}**")

                st.audio(recommendation["spotify_preview_url"])
                st.write("---")
        else:
            st.write(f"Sorry, we couldn't find {song_name} in our database. Please try another song.")

elif filtering_type == "Hybrid Recommender System":
    if st.button("Get Recommendations"):
        st.write("Recommendations for", f"**{song_name}** by **{artist_name}**")
        recommender = HybridRecommenderSystem(
            number_of_recommendations=k,
            weight_content_based=content_based_weight,
        )
        recommendations = recommender.give_recommendations(
            song_name=song_name,
            artist_name=artist_name,
            songs_data=filtered_data,
            transformed_matrix=transformed_hybrid_data,
            track_ids=track_ids,
            interaction_matrix=interaction_matrix,
        )

        for ind, recommendation in recommendations.iterrows():
            recommendation_name = recommendation["name"].title()
            recommendation_artist = recommendation["artist"].title()

            if ind == 0:
                st.markdown("## Currently Playing")
                st.markdown(f"#### **{recommendation_name}** by **{recommendation_artist}**")
            elif ind == 1:
                st.markdown("### Next Up")
                st.markdown(f"#### {ind}. **{recommendation_name}** by **{recommendation_artist}**")
            else:
                st.markdown(f"#### {ind}. **{recommendation_name}** by **{recommendation_artist}**")

            st.audio(recommendation["spotify_preview_url"])
            st.write("---")
