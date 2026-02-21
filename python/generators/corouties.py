from typing import Generator, Any

def anomaly_filter(limit: float, next_step: Generator) -> Generator[None, float, None]:
    """
    Receives data via .send(). If the data is less than the limit, 
    it passes it on to the next stage of the pipeline.
    """
    try:
        while True:
            value = yield  
            
            if value <= limit:
                next_step.send(value)
            else:
                print(f"[FILTER] Anomaly detected and ignored: {value}")
    except GeneratorExit:
        print("[FILTER] Closing filter coroutine...")

def media_movel() -> Generator[None, float, None]:
    """
    Maintains state (total and quantity) in memory indefinitely
    without needing to instantiate a Class.
    """

    total = 0.0
    amount = 0
    try:
        while True:
            new_value = yield 
            total += new_value
            amount += 1
            media = total / amount
            print(f" ->Data processed: {new_value:.2f} | Current Moving Average: {media:.2f}")
    except GeneratorExit:
        print("[MÉDIA] Closing media moving average coroutine...")

def start_coroutine(coro: Generator) -> Generator:
    """
    To use .send() for the first time, the coroutine needs to be paused at 'yield'.
    The next() makes it run until it hits the first yield (we call this 'priming')..
    """
    next(coro)
    return coro


if __name__ == "__main__":
    average_calculator = start_coroutine(media_movel())
    filter_test        = start_coroutine(anomaly_filter(limit=28.0, next_step=average_calculator))

    real_time_data = [25.5, 26.0, 30.5, 24.8, 40.0, 25.0]
    
    for data in real_time_data:
        print(f"\nSend data: {data}")
        filter_test.send(data)

    filter_test.close()
    average_calculator.close()