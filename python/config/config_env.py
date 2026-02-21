import os
import dotenv
from pathlib import Path
from typing import Dict

class EnvConfigManager:
    """Manages an environment variables (.env) file with automatic backups."""
    
    def __init__(self, filepath: str, default_vars: Dict[str, str]):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        
        self.default_vars = default_vars
        self._ensure_exists()
        
        dotenv.load_dotenv(self.filepath)

    def _ensure_exists(self) -> None:
        if not self.filepath.exists():
            print(f"[ENV] Secret file not found. Creating default at '{self.filepath}'")
            self._write_defaults()

    def _write_defaults(self) -> None:
        """Manually creates the .env file structure."""
        with open(self.filepath, 'w', encoding='utf-8') as file:
            for key, value in self.default_vars.items():
                file.write(f"{key}={value}\n")

    def get_secret(self, key: str) -> str:
        """Retrieves the secret directly from the loaded OS environment."""
        return os.getenv(key, "NOT_FOUND")

if __name__ == "__main__":
    # Use empty or dummy strings for defaults. NEVER hardcode real passwords here.
    DEFAULT_SECRETS = {
        "OPENROUTER_API_KEY": "change_me_immediately",
        "DATABASE_PASSWORD": "change_me_immediately"
    }

    env_manager = EnvConfigManager("CONFIG/.env", DEFAULT_SECRETS)
    
    api_key = os.getenv("OPENROUTER_API_KEY", "NOT_FOUND")
    print(f"Loaded API Key: {api_key}")