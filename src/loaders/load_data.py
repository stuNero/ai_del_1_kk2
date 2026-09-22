from contextlib import closing
from pathlib import Path
import pandas as pd
import io, zipfile, requests, sqlite3, logging, sys
from src.config.paths import DB_PATH, DATASET_FALLBACK_PATH
from src.config.constants import REG_RAW_TABLE_NAME, KAGGLE_DATASET_URL

logger = logging.getLogger(__name__)

def load_dataset(url: str = KAGGLE_DATASET_URL) -> pd.DataFrame:

    def fetch_url(url: str) -> zipfile:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response._content
        except requests.exceptions.RequestException as error:
            raise ConnectionError(f"Could not download dataset: {error}. Try downloading the ZIP file and put it in the root folder") from error
    
    def fetch_file(path: str | Path = DATASET_FALLBACK_PATH ) -> bytes:
        try:
            return Path(path).read_bytes()
        except OSError as error:
            raise ConnectionError(f"Could not read dataset file: {error}") from error
    
    if isinstance(url, str) and url.startswith(("http://", "https://")):
        dataset_content = fetch_url(url)
    else:
        dataset_content = fetch_file(DATASET_FALLBACK_PATH)
    
    try:
        with zipfile.ZipFile(io.BytesIO(dataset_content)) as z:
            print ("Files", z.namelist())
            
            csv_name = next(name for name in z.namelist() if name.lower().endswith(".csv"))
            
            df = pd.read_csv(z.open(csv_name))
            
            return df
    except (zipfile.BadZipFile, StopIteration, pd.errors.ParserError) as error:
        raise ValueError(f"Invalid dataset archive: {error}") from error

def save_to_db(df:pd.DataFrame, db_path:Path=DB_PATH, table_name:str=REG_RAW_TABLE_NAME):
    db_path = Path(db_path)
    db_existed = db_path.exists()

    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(db_path)) as connection:
            df.to_sql(table_name, connection, if_exists="replace", index=False)
            connection.commit()
    except Exception as e:
        raise ConnectionError(f'Error while saving to database: "{e}"') from e

    if not db_existed:
        print(f"Database [{db_path.name}] created!")
    print(f"Table [{table_name}] in database [{db_path.name}] saved successfully!")

def load_from_db(db_path:Path=DB_PATH, table_name:str=REG_RAW_TABLE_NAME) -> pd.DataFrame:
    try:
        with closing(sqlite3.connect(db_path)) as conn:
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    except Exception as e:
        raise ConnectionError(f"Error while loading from database: {e}" ) from e
    return df

def run_pipeline(db_path:Path=DB_PATH):
    
    df = load_dataset()
    
    save_to_db(df, db_path=db_path)

if __name__ == "__main__":
    run_pipeline(db_path=DB_PATH)