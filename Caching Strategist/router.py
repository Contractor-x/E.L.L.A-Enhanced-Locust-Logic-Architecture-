import threading
import queue
import time
from collections import OrderedDict

# Queues for requests and results
data_queue = queue.Queue()
result_queue = queue.Queue()

# LRU Cache config
CACHE_SIZE = 5  # Max cache entries
CACHE_TTL = 10  # seconds

# LRU Cache storage
class LRUCache:
    def __init__(self, max_size):
        self.cache = OrderedDict()
        self.max_size = max_size

    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache.pop(key)
            if time.time() - timestamp < CACHE_TTL:
                self.cache[key] = (value, time.time())  # Refresh usage
                return value
        return None

    def put(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)  # Pop least recently used
        self.cache[key] = (value, time.time())

cache = LRUCache(CACHE_SIZE)

# Threaded worker function
def data_worker(source_id):
    while True:
        try:
            request = data_queue.get(timeout=2)
            result = cache.get(request)
            if result:
                print(f"[Cache Hit] {request}")
            else:
                print(f"[Thread-{source_id}] Fetching {request} from source...")
                time.sleep(0.2)  # Simulated DB call
                result = f"Result from Source-{source_id} for {request}"
                cache.put(request, result)
            result_queue.put(result)
            data_queue.task_done()
        except queue.Empty:
            break

def run_router(num_sources=3):
    threads = []
    for i in range(num_sources):
        t = threading.Thread(target=data_worker, args=(i,))
        t.start()
        threads.append(t)

    # Simulate data requests
    sample_requests = ['DataRequest-1', 'DataRequest-2', 'DataRequest-3',
                       'DataRequest-4', 'DataRequest-1', 'DataRequest-5',
                       'DataRequest-6', 'DataRequest-2', 'DataRequest-7', 'DataRequest-8']

    for req in sample_requests:
        data_queue.put(req)

    data_queue.join()

    for t in threads:
        t.join()

    while not result_queue.empty():
        print(result_queue.get())
