from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "db" / "burnout_database.db"
DATA_PATH = PROJECT_ROOT / "data" / "mental_health_burnout_prediction_dataset.csv"
