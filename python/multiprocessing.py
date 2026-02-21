import multiprocessing
import time
import ctypes
from typing import Any

def process_sensor_chunk(
    worker_id: int,
    start_idx: int, 
    end_idx: int, 
    shared_array: Any, 
    shared_counter: Any, 
    lock: Any
) -> None:
    """
    This function runs on a completely separate CPU core.
    It reads and writes directly to a shared block of C-level memory,
    bypassing the need to serialize (pickle) and copy data between processes.
    """
    print(f"[WORKER-{worker_id}] Starting heavy computation on indices {start_idx} to {end_idx - 1}...")
    
    # Simulating a heavy CPU-bound mathematical operation (e.g., matrix transformations)
    for i in range(start_idx, end_idx):
        # Reading from the shared C-array
        raw_value = shared_array[i]
        
        # Heavy math simulation
        processed_value = (raw_value * 3.14159) ** 1.5 
        
        # Writing directly back to the shared memory block
        shared_array[i] = processed_value
        
    # Safely updating a shared variable. 
    # Without the lock, two workers might update it at the exact same millisecond, 
    # causing a race condition where 1 + 1 = 1.
    with lock:
        shared_counter.value += 1
        print(f"[WORKER-{worker_id}] Finished. Total chunks completed globally: {shared_counter.value}")


if __name__ == "__main__":

    ARRAY_SIZE = 100
    print(f"[SYSTEM] Allocating shared memory array of size {ARRAY_SIZE}...")
    shared_sensor_data = multiprocessing.Array(ctypes.c_double, ARRAY_SIZE)
    
    for i in range(ARRAY_SIZE):
        shared_sensor_data[i] = float(i)

    tasks_completed = multiprocessing.Value(ctypes.c_int, 0)
    
    memory_lock = multiprocessing.Lock()

    # Let's split the 100 elements into 4 chunks of 25 to run on 4 separate cores.
    NUM_WORKERS = 4
    chunk_size = ARRAY_SIZE // NUM_WORKERS
    processes: list[multiprocessing.Process] = []

    start_time = time.perf_counter()

    for i in range(NUM_WORKERS):
        start_index = i * chunk_size
        end_index = start_index + chunk_size
        
        p = multiprocessing.Process(
            target=process_sensor_chunk,
            args=(i, start_index, end_index, shared_sensor_data, tasks_completed, memory_lock)
        )
        processes.append(p)
        p.start() 

    print(f"[SYSTEM] Dispatched {NUM_WORKERS} concurrent processes.")

    # The main script must wait for all child processes to finish before continuing.
    for p in processes:
        p.join()

    elapsed_time = time.perf_counter() - start_time

    print(f"\n[SYSTEM] All processes completed in {elapsed_time:.4f} seconds.")
    print(f"[SYSTEM] Shared Counter Value: {tasks_completed.value}")