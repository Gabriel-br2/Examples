import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class JsonConfigManager:
    """Manages a JSON configuration file with automatic backups."""
    
    def __init__(self, filepath: str, default_config: Dict[str, Any]):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True) # Ensure directory exists
        
        self.default_config = default_config
        self._ensure_exists()

    def _ensure_exists(self) -> None:
        """Creates the file with default values if it doesn't exist."""
        
        
        if not self.filepath.exists():
            print(f"[JSON] Config file not found. Creating default at '{self.filepath}'")
            self.update_all(self.default_config, create_backup=False)

    def _create_backup(self) -> None:
        """Copies the current file to a timestamped backup."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # e.g., settings.json -> settings_20260221_143000.json.bak
        backup_name = f"{self.filepath.stem}_{timestamp}{self.filepath.suffix}.bak"
        backup_path = self.filepath.parent / backup_name
        
        shutil.copy2(self.filepath, backup_path) # copy2 preserves file metadata
        print(f"[JSON] Backup created: {backup_name}")

    def load(self) -> Dict[str, Any]:
        """Reads and returns the JSON configuration."""
        with open(self.filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    def update_all(self, new_config: Dict[str, Any], create_backup: bool = True) -> None:
        """Overwrites the entire configuration, creating a backup first."""
        if create_backup and self.filepath.exists():
            self._create_backup()
            
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(new_config, file, indent=4, sort_keys=True)
        print(f"[JSON] Configuration saved successfully to '{self.filepath.name}'.")

    def update_key(self, key: str, value: Any) -> None:
        """Updates a single key in real-time."""
        config = self.load()
        config[key] = value
        self.update_all(config)


if __name__ == "__main__":
    DEFAULT_JSON_PAYLOAD = {
        "robot_id": "ARM_116",
        "kinematics": {"max_velocity": 1.5, "max_acceleration": 0.8},
        "active_modules": ["vision", "telemetry"]
    }

    json_manager = JsonConfigManager("CONFIG/config.json", DEFAULT_JSON_PAYLOAD)
    
    # Reading
    current_cfg = json_manager.load()
    print(f"Current Velocity: {current_cfg['kinematics']['max_velocity']}")
    
    # Real-time Update (This will trigger a backup)
    current_cfg['kinematics']['max_velocity'] = 2.0
    json_manager.update_all(current_cfg)