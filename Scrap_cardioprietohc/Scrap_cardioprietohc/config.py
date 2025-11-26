import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class Settings:
    base_url: str
    username: str
    password: str
    output_dir: Path


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", BASE_DIR / "data" / "raw"))

settings = Settings(
    base_url=os.getenv("BASE_URL", ""),
    username=os.getenv("USERNAME", ""),
    password=os.getenv("PASSWORD", ""),
    output_dir=OUTPUT_DIR,
)

# Crear carpetas de salida si no existen
settings.output_dir.mkdir(parents=True, exist_ok=True)
