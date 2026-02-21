import asyncio
import time
from typing import List, AsyncGenerator, Dict, Any

# We limit the system to process a maximum of 3 concurrent network requests.
# If 10 tasks are created, 3 will run, and 7 will wait in line.
MAX_CONCURRENT_CONNECTIONS = 3
network_semaphore = asyncio.Semaphore(MAX_CONCURRENT_CONNECTIONS)

async def fetch_sensor_data_over_network(sensor_id: int, delay: float) -> Dict[str, Any]:
    """
    Simulates a network-bound I/O operation.
    The 'async with' ensures the task waits for a green light from the semaphore.
    """
    async with network_semaphore:
        print(f"[NETWORK] Sensor {sensor_id} connecting... (Semaphore acquired)")
        
        # CRITICAL: We use asyncio.sleep(), NOT time.sleep()!
        # time.sleep() would freeze the entire program. 
        # asyncio.sleep() pauses ONLY this function and hands control back to the Event Loop.
        await asyncio.sleep(delay) 
        
        print(f"[NETWORK] Sensor {sensor_id} finished downloading. (Semaphore released)")
        return {"sensor_id": sensor_id, "payload": delay * 100.0}


async def live_data_stream(num_readings: int) -> AsyncGenerator[float, None]:
    """
    Simulates a live WebSocket or serial data stream.
    Yields data asynchronously as it arrives over time.
    """
    for index in range(num_readings):
        # Waiting for the next packet of data to arrive over the network
        await asyncio.sleep(0.4) 
        
        # Yielding the data back to the consumer
        yield 25.0 + (index * 0.5)


async def consume_live_stream() -> None:
    """Consumes the asynchronous generator using 'async for'."""
    print("\n[STREAM] Opening live data connection...")
    
    # 'async for' waits automatically for the next 'yield' from the generator
    async for reading in live_data_stream(num_readings=4):
        print(f" -> Live reading received: {reading:.2f} °C")
        
    print("[STREAM] Connection closed by the server.")


async def main() -> None:
    start_time = time.perf_counter()    
    tasks: List[asyncio.Task] = []
    
    for i in range(1, 9):
        simulated_network_delay = 1.0 
        task = asyncio.create_task(fetch_sensor_data_over_network(i, simulated_network_delay))
        tasks.append(task)
        
    print(f"[SYSTEM] Successfully scheduled {len(tasks)} tasks in the background.")
    
    # asyncio.gather suspends 'main()' until ALL tasks in the list have finished.
    # It returns a list of results in the exact order the tasks were created.
    results = await asyncio.gather(*tasks)
    
    elapsed_time = time.perf_counter() - start_time
    print(f"\n[SYSTEM] All {len(results)} requests completed in {elapsed_time:.2f} seconds.")
    print(f"[SYSTEM] Data Extracted: {results}")


    print("\n--- 2. Testing Asynchronous Generators ---")
    # Awaiting the stream consumer to start the 'async for' loop
    await consume_live_stream()


if __name__ == "__main__":
    asyncio.run(main())