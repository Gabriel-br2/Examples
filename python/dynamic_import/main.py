import importlib.util
from pathlib import Path
from registry import ACTIVE_DRIVERS

def load_plugins(directory: str) -> None:
    path = Path(directory)
    
    if not path.exists() or not path.is_dir():
        print(f"[ERROR] Directory '{directory}' not found. Create the folder and add files.")
        return

    print(f"[SYSTEM] Starting plugin scan in: {directory}/")
    
    for py_file in path.glob("*.py"):
        if py_file.name == "__init__.py":
            continue
            
        module_name = py_file.stem
        
        spec = importlib.util.spec_from_file_location(module_name, py_file)
        
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            
            try:
                spec.loader.exec_module(module)
                print(f"  -> Module '{module_name}' loaded successfully.")
            except Exception as e:
                print(f"  -> [FAILED] Error loading module '{module_name}': {e}")

if __name__ == "__main__":
    load_plugins("plugins")
    
    print("\n[SYSTEM] Drivers registered and ready to use:")
    for driver_name in ACTIVE_DRIVERS.keys():
        print(f" - {driver_name}")
        
    print("\n[SYSTEM] Requesting readings from all connected sensors:")
    
    for name, reading_function in ACTIVE_DRIVERS.items():
        try:
            data = reading_function()
            print(f"[{name}] Reading: {data['value']} {data['unit']}")
        except Exception as e:
            print(f"[{name}] Reading error: {e}")