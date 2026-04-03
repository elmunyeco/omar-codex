import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class Settings:
    base_url: str  # Origen, ej: https://cardioprietohc.com/
    username: str
    password: str
    output_dir: Path
    login_path: str
    pacientes_path: str
    historias_path: str
    pacientes_max_pages: int


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", BASE_DIR / "data" / "raw"))

settings = Settings(
    base_url=os.getenv("BASE_URL", "").rstrip("/") + "/",
    username=os.getenv("USERNAME", ""),
    password=os.getenv("PASSWORD", ""),
    output_dir=OUTPUT_DIR,
    login_path=os.getenv("LOGIN_PATH", ""),
    pacientes_path=os.getenv("PACIENTES_PATH", "/index.php/pacientes/index"),
    historias_path=os.getenv("HISTORIAS_PATH", "/index.php/historias/index"),
    pacientes_max_pages=int(os.getenv("PACIENTES_MAX_PAGES", "3")),
)

# Crear carpetas de salida si no existen
settings.output_dir.mkdir(parents=True, exist_ok=True)
