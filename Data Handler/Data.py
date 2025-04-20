"""
PROJECT E.L.L.A: Threaded System Guide for V3 - Data Handler
Role: Threaded Data Router + Fallback System
"""

import threading
import queue
import time
import logging
import random

# === Phase 1: Mission Boot ===
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# === Phase 2: Queue Setup ===
data_queue = queue.Queue()
result_queue = queue.Queue()

# === Phase 3: Fallback Logic ===
def fallback_fetch(primary, backup_data):
    try:
        raise ConnectionError("Primary failed")
    except Exception as e:
        logging.warning(f"Primary source failed: {e}. Switching to backup...")
        return f"Recovered from Backup for {primary} -> {backup_data}"

# === Phase 4: Simulated Fetch ===
def fetch_from_primary(source_id, request):
    if random.random() < 0.3:  # Simulate 30% failure rate
        raise Exception("Simulated Failure")
    time.sleep(random.uniform(0.2, 0.4))
    return f"Primary Result from Source-{source_id} for {request}"

def fetch_from_backup(source_id, request):
    time.sleep(random.uniform(0.1, 0.2))
    return f"Backup Result from Source-{source_id} for {request}"

# === Phase 5: Worker Thread ===
def data_worker(source_id):
    while True:
        try:
            request = data_queue.get(timeout=2)
            start = time.perf_counter()

            try:
                result = fetch_from_primary(source_id, request)
                logging.info(f"[Source-{source_id}] Primary Success: {request}")
            except Exception:
                backup = fetch_from_backup(source_id, request)
                result = fallback_fetch(request, backup)

            elapsed = time.perf_counter() - start
            logging.info(f"[Source-{source_id}] ⏱️ Processed {request} in {elapsed:.2f}s")

            result_queue.put(result)
            data_queue.task_done()
        except queue.Empty:
            break

# === Phase 6: Router Controller ===
def run_router(num_sources=3, num_requests=10):
    threads = []

    for i in range(num_sources):
        t = threading.Thread(target=data_worker, args=(i,))
        t.start()
        threads.append(t)

    for request_id in range(num_requests):
        data_queue.put(f"DataRequest-{request_id}")

    data_queue.join()

    for t in threads:
        t.join()

    print("\n Results:")
    while not result_queue.empty():
        print("🔹", result_queue.get())

# === Phase 7: Entry Point ===
if __name__ == "__main__":
    logging.info("E.L.L.A V3: Threaded Data Handler Initializing...")
    run_router(num_sources=4, num_requests=15)
    logging.info("All tasks completed. Mission success.")
