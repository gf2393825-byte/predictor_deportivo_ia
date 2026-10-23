import os 
from pathlib import Path 
from dotenv import load_dotenv 
BASE_DIR = Path(__file__).resolve().parent.parent 
load_dotenv(BASE_DIR / ".env") 
class Settings: 
    DATA_RAW_DIR: Path = BASE_DIR / "data" / "raw" 
    DATA_PROCESSED_DIR: Path = BASE_DIR / "data" / "processed" 
    DB_PATH: Path = BASE_DIR / os.getenv("DB_PATH", "data/processed/predictor.db") 
    API_FOOTBALL_KEY: str = os.getenv("API_FOOTBALL_KEY", "") 
    ODDS_API_KEY: str = os.getenv("ODDS_API_KEY", "") 
    DECAY_LAMBDA: float = 0.005 
    MIN_HISTORICAL_MATCHES: int = 10 
settings = Settings()
