from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "db" / "burnout_database.db"
APP_PATH = PROJECT_ROOT / "src" / "app" / "app.py"
ENDPOINTS_MODULE = "src.api.endpoints:app"