# Spotify Hybrid Recommender System

This project now runs locally without AWS, ECR, S3, CodeDeploy, or DVC pulls.

## Data note

The large raw dataset files are intentionally not stored in GitHub because `data/User Listening History.csv` exceeds GitHub's regular file-size limits.

This repository includes the smaller derived artifacts needed to run the app directly.

If you want to rebuild those artifacts from scratch, place these raw files in `data/`:

- `Music Info.csv`
- `User Listening History.csv`

## Run locally

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the Streamlit app:

```bash
streamlit run app.py --server.port 8000
```

If the derived artifacts are missing, the app automatically rebuilds them from:

- `data/Music Info.csv`
- `data/User Listening History.csv`

That first startup can take a few minutes because it generates the recommendation artifacts locally.

## Test locally

Start the app on port `8000`, then run:

```bash
pytest test_app.py
```

## Deploy for free

### Best fit: Streamlit Community Cloud

This is the easiest option for this app because it is a native Streamlit host.

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Click `Create app`.
4. Select your repository, branch, and `app.py` as the entrypoint.
5. In advanced settings, choose Python `3.12`.
6. Deploy.

Notes:

- Streamlit Community Cloud is free.
- This repository already includes the smaller generated artifacts needed for startup.
- If you remove those artifacts and want to rebuild them, you will need the raw dataset files locally.

### More general cloud option: Render

This repo includes [`render.yaml`](render.yaml), so Render can deploy it as a free Python web service.

1. Push this repository to GitHub.
2. In Render, create a new `Web Service`.
3. Connect the repository.
4. Render should detect the settings from `render.yaml`.
5. If prompted manually, use:

```bash
Build Command:
pip install -r requirements.txt && python -c "from local_data import ensure_local_artifacts; print(ensure_local_artifacts())"
```

```bash
Start Command:
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true
```

Notes:

- Render free web services spin down after inactivity.
- This repository already includes the smaller generated artifacts needed for startup.
- If you remove those artifacts and want to rebuild them, you will need the raw dataset files locally.
- This app is better suited to Render or Streamlit Community Cloud than Netlify or Vercel because it needs a long-running Python web process, not only serverless functions.

### Heroku

This repository is now set up for Heroku with:

- `Procfile` for the Streamlit web process
- `.python-version` set to `3.12`
- `app.json` for app metadata
- `.slugignore` to keep the deploy slug smaller

Deploy steps:

```bash
heroku login
heroku create your-app-name
git push heroku master
heroku open
```

Useful commands:

```bash
heroku logs --tail --app your-app-name
heroku ps --app your-app-name
```
