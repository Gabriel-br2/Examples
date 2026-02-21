import yaml # Requires: pip install pyyaml
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class YamlConfigManager:
    """Manages a YAML configuration file with automatic backups."""
    
    def __init__(self, filepath: str, default_config: Dict[str, Any]):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True) # Ensure directory exists
        
        self.default_config = default_config
        self._ensure_exists()

    def _ensure_exists(self) -> None:
        if not self.filepath.exists():
            print(f"[YAML] Config file not found. Creating default at '{self.filepath}'")
            self.update_all(self.default_config, create_backup=False)

    def _create_backup(self) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{self.filepath.stem}_{timestamp}{self.filepath.suffix}.bak"
        backup_path = self.filepath.parent / backup_name
        shutil.copy2(self.filepath, backup_path)
        print(f"[YAML] Backup created: {backup_name}")

    def load(self) -> Dict[str, Any]:
        with open(self.filepath, 'r', encoding='utf-8') as file:
            # Safe load prevents arbitrary Python code execution from YAML files
            return yaml.safe_load(file) or {}

    def update_all(self, new_config: Dict[str, Any], create_backup: bool = True) -> None:
        if create_backup and self.filepath.exists():
            self._create_backup()
            
        with open(self.filepath, 'w', encoding='utf-8') as file:
            # default_flow_style=False ensures the clean block-style YAML format
            yaml.dump(new_config, file, default_flow_style=False, sort_keys=False)
        print(f"[YAML] Configuration saved successfully to '{self.filepath.name}'.")


if __name__ == "__main__":
    DEFAULT_YAML_PAYLOAD = {
        "mqtt_broker": {
            "host": "192.168.1.100",
            "port": 1883,
            "topics": ["sensors/temp", "robot/status"]
        },
        "log_level": "DEBUG"
    }

    yaml_manager = YamlConfigManager("CONFIG/settings.yaml", DEFAULT_YAML_PAYLOAD)
    
    config = yaml_manager.load()
    print(f"MQTT Host: {config['mqtt_broker']['host']}")
    
    # Updating
    config['mqtt_broker']['port'] = 8883 # Changing to secure MQTT port
    yaml_manager.update_all(config)