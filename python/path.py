from pathlib import Path

def setup_directory(dir_name: str) -> Path:
    """
    Creates a new directory in the current working directory.
    Returns the Path object of the created directory.
    """
    current_dir = Path('.')
    new_dir = current_dir / dir_name
    
    # exist_ok=True prevents raising an error if the directory already exists
    new_dir.mkdir(exist_ok=True)
    print(f"Directory ready: {new_dir.resolve()}")
    
    return new_dir

def create_and_read_file(dir_path: Path, file_name: str) -> Path:
    """
    Creates a text file inside the given directory, writes sample text, 
    reads it back, and returns the file's Path object.
    """
    file_path = dir_path / file_name

    # Write text to the file
    file_path.write_text(
        'Hello! This is a test using the pathlib library.\nSecond line here.', 
        encoding='utf-8'
    )
    
    # Read the content back
    content = file_path.read_text(encoding='utf-8')
    print(f"\n--- Content of '{file_name}' ---")
    print(content)
    
    return file_path

def display_file_info(file_path: Path) -> None:
    """
    Checks if the file exists and prints useful metadata.
    """
    if file_path.exists():
        print("\n--- FILE INFORMATION ---")
        print(f"File name: {file_path.name}")
        print(f"Stem (name without extension): {file_path.stem}")
        print(f"Suffix (extension): {file_path.suffix}")
        print(f"Absolute path: {file_path.resolve()}")
        print("-" * 24)

def list_text_files(dir_path: Path) -> None:
    """
    Lists all .txt files in the specified directory.
    """
    print(f"\nListing .txt files in '{dir_path.name}':")
    for file in dir_path.glob('*.txt'):
        print(f"- {file.name}")

def main():
    target_directory = 'my_test_directory'
    target_file = 'example.txt'

    test_dir = setup_directory(target_directory)

    test_file = create_and_read_file(test_dir, target_file)

    display_file_info(test_file)

    list_text_files(test_dir)

if __name__ == "__main__":
    main()