from typing import Generator, Any

def flatten_data_packets(packets: list) -> Generator[Any, None, None]:
    """
    yield from' takes an iterable (like a list inside another list) 
    and recursively delegates the yield to it. It avoids multiple nested 'for' loops.
    """
    for item in packets:
        if isinstance(item, list):
            yield from flatten_data_packets(item)
        else:
            yield item

if __name__ == "__main__":
    dirty_packages = [24.5, [25.1, 26.0, [24.9, 25.5]], 23.8]
    clean_data = list(flatten_data_packets(dirty_packages))
    print(f"dirty_packages: {dirty_packages}")
    print(f"clean_data:   {clean_data}")
