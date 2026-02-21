from typing import Generator, Any

def reads_generator(max_reads: int) -> Generator[float, None, None]:
    """
    Generates data on demand. Doesn't load everything into memory.
    Excellent for reading large files or continuous streams.    """
    import random

    for i in range(max_reads):
        # Simulates the reading of a temperature sensor with some noise.
    
        read = 25.0 + random.uniform(-2.0, 2.0)
        yield round(read, 2)

if __name__ == "__main__":
    sensor = reads_generator(3)

    print(next(sensor))
    print(next(sensor))
    print(next(sensor))
    #print(next(sensor)) # This would cause StopIteration, as the generator has already finished 
    