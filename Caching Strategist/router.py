import threading
import queue
import time

# Queues for managing requests and results
data_queue = queue.Queue()
result_queue = queue.Queue()

# Cache with optional expiration support
cache = {}
cache_expiry = {}
CACHE_TTL = 10  # seconds

def is_cache_valid(key):
    return key in cache and (time.time() - cache_expiry[key] < CACHE_TTL)

def data_worker(source_id):
    while True:
        try:
            request = data_queue.get(timeout=2)

            if is_cache_valid(request):
                result = cache[request]
                print(f"[Cache] Hit: {request}")
            else:
                print(f"[Source-{source_id}] Fetching: {request}")
                # Simulate data retrieval delay
                time.sleep(0.3)
                result = f"Result from Source-{source_id} for {request}"
                cache[request] = result
                cache_expiry[request] = time.time()

            result_queue.put(result)
            data_queue.task_done()

        except queue.Empty:
            break

def run_router(num_sources=3):
    threads = [threading.Thread(target=data_worker, args=(i,)) for i in range(num_sources)]
    for t in threads:
        t.start()

    # Simulate data requests with repeated entries
    for i in range(5):
        for j in range(2):  # Duplicate requests to test cache
            data_queue.put(f"DataRequest-{i}")

    data_queue.join()

    for t in threads:
        t.join()

    while not result_queue.empty():
        print(result_queue.get())
