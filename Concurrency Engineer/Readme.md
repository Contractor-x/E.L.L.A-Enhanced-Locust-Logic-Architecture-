# PROJECT E.L.L.A: Threaded System Guide for V3 - Concurrency Engineer

**Role Objective:**
To build a multi-threaded, high-speed data router and fallback recovery mechanism inspired by the parallelism in locust neural systems.

---

### Phase 1: Understanding the Mission

- **Goal**: Design and implement a threaded data recovery and routing system that:
  - Prioritizes speed
  - Avoids blocking I/O
  - Enables fallback to alternative nodes if primary data retrieval fails

---

### Phase 2: Environment Setup

**Requirements:**

- Python 3.10+
- Use built-in `threading` and `queue` libraries (no external dependencies)

```bash
python3 -m venv ella_env
source ella_env/bin/activate
pip install --upgrade pip
```

---

### Phase 3: Threaded Router (`router.py`)

#### 1. Import Essentials

```python
import threading
import queue
import time
```

#### 2. Define Global Queues

```python
data_queue = queue.Queue()
result_queue = queue.Queue()
```

#### 3. Worker Thread Function

```python
def data_worker(source_id):
    while True:
        try:
            request = data_queue.get(timeout=2)
            print(f"[Source-{source_id}] Handling: {request}")
            # Simulate data fetch
            time.sleep(0.5)
            result = f"Result from Source-{source_id} for {request}"
            result_queue.put(result)
            data_queue.task_done()
        except queue.Empty:
            break
```

#### 4. Thread Initialization Function

```python
def run_router(num_sources=3):
    threads = []
    for i in range(num_sources):
        t = threading.Thread(target=data_worker, args=(i,))
        t.start()
        threads.append(t)
    
    for request_id in range(10):
        data_queue.put(f"DataRequest-{request_id}")

    data_queue.join()
    for t in threads:
        t.join()

    while not result_queue.empty():
        print(result_queue.get())
```

---

### Phase 4: Fallback System (`fallback_recovery.py`)

#### 1. Design Fallback Logic

```python
def fallback_fetch(primary, backup):
    try:
        # Simulate primary failure
        raise ConnectionError("Primary failed")
    except Exception as e:
        print(f"Primary source failed: {e}. Switching to backup...")
        return f"Recovered from Backup for {primary}"
```

#### 2. Integrate into Router (Optional Override)

- Modify `data_worker` to include fallback logic if primary retrieval fails

---

### Phase 5: Integration and Testing

- Use `main.py` to test integration

```python
from router import run_router

if __name__ == "__main__":
    run_router()
```

---

### Phase 6: Optimization Ideas

- ThreadPoolExecutor for dynamic scaling
- Logging instead of print
- Add timeout and retry limits
- Profile time with `time.perf_counter()`

---

### Mission Status: In Progress ✅

*Complete your unit test plan, document thread behavior, and simulate errors to verify fallback triggers properly.*
---

# Please make sure to upload your code on Github for Review
