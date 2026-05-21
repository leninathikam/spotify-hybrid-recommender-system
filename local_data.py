from pathlib import Path

from collaborative_filtering import main as build_collaborative_artifacts
from content_based_filtering import CLEANED_DATA_PATH, main as build_content_artifacts
from data_cleaning import DATA_PATH, main as build_cleaned_data
from transform_filtered_data import filtered_data_path, main as build_hybrid_artifacts, save_path


PROJECT_ROOT = Path(__file__).resolve().parent
TRANSFORMER_PATH = PROJECT_ROOT / "transformer.joblib"
RAW_DATA_FILES = [
    PROJECT_ROOT / DATA_PATH,
    PROJECT_ROOT / "data" / "User Listening History.csv",
]
REQUIRED_ARTIFACTS = [
    PROJECT_ROOT / CLEANED_DATA_PATH,
    PROJECT_ROOT / "data" / "transformed_data.npz",
    PROJECT_ROOT / "data" / "track_ids.npy",
    PROJECT_ROOT / filtered_data_path,
    PROJECT_ROOT / "data" / "interaction_matrix.npz",
    PROJECT_ROOT / save_path,
    TRANSFORMER_PATH,
]


def _missing_paths(paths: list[Path]) -> list[Path]:
    return [path for path in paths if not path.exists()]


def ensure_local_artifacts() -> list[str]:
    if not _missing_paths(REQUIRED_ARTIFACTS):
        return []

    missing_raw_data = _missing_paths(RAW_DATA_FILES)
    if missing_raw_data:
        missing_display = ", ".join(str(path.relative_to(PROJECT_ROOT)) for path in missing_raw_data)
        raise FileNotFoundError(
            "Missing raw data files needed to rebuild artifacts: "
            f"{missing_display}"
        )

    generated_steps: list[str] = []

    cleaned_data_path = PROJECT_ROOT / CLEANED_DATA_PATH
    if not cleaned_data_path.exists():
        build_cleaned_data(str(PROJECT_ROOT / DATA_PATH))
        generated_steps.append("cleaned_data")

    transformed_data_path = PROJECT_ROOT / "data" / "transformed_data.npz"
    if not transformed_data_path.exists() or not TRANSFORMER_PATH.exists():
        build_content_artifacts(str(cleaned_data_path))
        generated_steps.append("content_features")

    collab_filtered_path = PROJECT_ROOT / filtered_data_path
    interaction_matrix_path = PROJECT_ROOT / "data" / "interaction_matrix.npz"
    track_ids_path = PROJECT_ROOT / "data" / "track_ids.npy"
    if (
        not collab_filtered_path.exists()
        or not interaction_matrix_path.exists()
        or not track_ids_path.exists()
    ):
        build_collaborative_artifacts()
        generated_steps.append("collaborative_features")

    transformed_hybrid_path = PROJECT_ROOT / save_path
    if not transformed_hybrid_path.exists():
        build_hybrid_artifacts(str(collab_filtered_path), str(transformed_hybrid_path))
        generated_steps.append("hybrid_features")

    remaining_missing = _missing_paths(REQUIRED_ARTIFACTS)
    if remaining_missing:
        missing_display = ", ".join(str(path.relative_to(PROJECT_ROOT)) for path in remaining_missing)
        raise RuntimeError(f"Unable to build required local artifacts: {missing_display}")

    return generated_steps
