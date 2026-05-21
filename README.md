# Spotify Hybrid Recommender System

This project implements a hybrid recommender system for Spotify songs, combining collaborative filtering and content-based filtering approaches. It leverages a large dataset of user listening history and song metadata to provide personalized song recommendations.

## Features

- **Collaborative Filtering:** Recommends songs based on user listening patterns using a sparse interaction matrix and cosine similarity.
- **Content-Based Filtering:** Suggests songs similar in audio features, tags, and metadata using feature engineering and vector similarity.
- **Hybrid Approach:** Integrates both methods for improved recommendation accuracy.
- **Data Cleaning & Transformation:** Preprocessing scripts for handling missing values, duplicates, and feature scaling.
- **Interactive Notebooks:** Jupyter notebooks for exploratory data analysis, model building, and evaluation.
- **Dockerized Deployment:** Easily deployable using Docker and AWS CodeDeploy.

## Project Structure

- `app.py` : Streamlit web app for serving recommendations.
- `collaborative_filtering.py` : Collaborative filtering logic.
- `content_based_filtering.py` : Content-based filtering logic.
- `hybrid_recommendations.py` : Hybrid recommendation logic.
- `data_cleaning.py` : Data preprocessing scripts.
- `transform_filtered_data.py` : Data transformation utilities.
- `notebooks/` : Jupyter notebooks for EDA and model development.
- `data/` : Data files and DVC tracking.
- `deploy/scripts/` : Deployment scripts for AWS.
- `requirements.txt` : Python dependencies.
- `Dockerfile` : Containerization setup.
- `.dvc/`, `.github/`, `.gitignore`, `.dvcignore` : Version control and CI/CD configs.

## Dataset

- **Music Info.csv**: Song metadata (track ID, name, artist, audio features, tags, etc.)
- **User Listening History.csv**: User-song interaction data (user ID, track ID, playcount).

Download automatically via [KaggleHub](https://github.com/kagglehub/kagglehub) in the notebooks.

## Getting Started

### Prerequisites

- Python 3.8+
- Docker (for deployment)
- [Kaggle API](https://github.com/Kaggle/kaggle-api) (for dataset access)
- [DVC](https://dvc.org/) (for data versioning)

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/spotify-hybrid-recommender-system.git
   cd spotify-hybrid-recommender-system
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Download the dataset:**
   - Run the notebooks in `notebooks/` or use the KaggleHub commands in the scripts.

4. **Run the app locally:**
   ```sh
   streamlit run app.py
   ```

### Docker Deployment

Build and run the Docker container:
```sh
docker build -t spotify-recommender .
docker run -p 8501:8501 spotify-recommender
```

### AWS Deployment

See [`appspec.yml`](appspec.yml) and scripts in [`deploy/scripts/`](deploy/scripts/) for CodeDeploy setup.

## Usage

- Use the Streamlit app to get song recommendations by entering a song name.
- Explore the Jupyter notebooks for data analysis and model details.

## Notebooks

- [`EDA_Spotify_Dataset.ipynb`](notebooks/EDA_Spotify_Dataset.ipynb): Exploratory Data Analysis.
- [`Spotify_Collaborative_Filtering.ipynb`](notebooks/Spotify_Collaborative_Filtering.ipynb): Collaborative filtering workflow.
- [`Spotify_Content_Based_Filtering.ipynb`](notebooks/Spotify_Content_Based_Filtering.ipynb): Content-based filtering workflow.

## Contributing

Pull requests are welcome! Please see the issues tab for open tasks.


## Acknowledgements

- [Kaggle Million Song Dataset](https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm)
- [DVC](https://dvc.org/)
- [Streamlit](https://streamlit.io/)
