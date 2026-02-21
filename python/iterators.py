from typing import List, Any

class DataBufferIterator:
    """
    The dedicated Iterator. It only knows how to point to a specific 
    index in a given data source and move forward.
    """
    def __init__(self, data_source: List[Any]):
        self._data_source = data_source
        self._cursor = 0

    def __iter__(self) -> 'DataBufferIterator':
        return self

    def __next__(self) -> Any:
        if self._cursor >= len(self._data_source):
            raise StopIteration
            
        value = self._data_source[self._cursor]
        self._cursor += 1
        return value


class ThreadSafeSensorBuffer:
    """
    The Iterable container. It holds the data, but it DOES NOT track iteration state.
    Every time you call __iter__, it spawns a completely new, independent Iterator.
    """
    def __init__(self):
        self._historical_data: List[float] = []

    def add_reading(self, reading: float) -> None:
        self._historical_data.append(reading)

    def __iter__(self) -> DataBufferIterator:
        """
        Returns a fresh iterator instance. This is the secret to allowing
        nested loops over the exact same object.
        """
        return DataBufferIterator(self._historical_data)


if __name__ == "__main__":    
    sensor_history = ThreadSafeSensorBuffer()
    sensor_history.add_reading(22.1)
    sensor_history.add_reading(22.5)
    sensor_history.add_reading(23.0)

    print("Executing nested loops over the SAME buffer object:")    
    for reading_a in sensor_history:
        print(f"[Loop A] Processing: {reading_a}")
        
        for reading_b in sensor_history:
            print(f"    -> [Loop B] Comparing with: {reading_b}")