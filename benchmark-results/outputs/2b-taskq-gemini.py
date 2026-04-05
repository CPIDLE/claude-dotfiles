import time
import uuid
import random
import threading
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any, Callable, Dict, List, Optional, Union

class TaskQueue:
    def __init__(self, max_workers: int = 4):
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def submit(self, fn: Callable, *args: Any, **kwargs: Any) -> str:
        task_id = str(uuid.uuid4())
        with self._lock:
            self._tasks[task_id] = {
                "id": task_id,
                "state": "pending",
                "result": None,
                "attempts": 0,
                "error": None
            }
        
        self._executor.submit(self._run_task, task_id, fn, *args, **kwargs)
        return task_id

    def _run_task(self, task_id: str, fn: Callable, *args: Any, **kwargs: Any) -> None:
        self._update_task(task_id, {"state": "running"})
        
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                self._update_task(task_id, {"attempts": attempt})
                result = fn(*args, **kwargs)
                self._update_task(task_id, {"state": "done", "result": result})
                return
            except Exception as e:
                self._update_task(task_id, {"error": str(e)})
                if attempt == max_retries:
                    self._update_task(task_id, {"state": "failed"})
                else:
                    time.sleep(2 ** (attempt - 1))
        
    def _update_task(self, task_id: str, updates: Dict[str, Any]) -> None:
        with self._lock:
            self._tasks[task_id].update(updates)

    def status(self, task_id: str) -> Dict[str, Any]:
        with self._lock:
            return self._tasks.get(task_id, {}).copy()

    def results(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._tasks.values())

def sample_task(n: int) -> str:
    if random.random() < 0.4:
        raise ValueError("Random failure")
    return f"Task {n} completed"

if __name__ == "__main__":
    tq = TaskQueue(max_workers=3)
    ids = [tq.submit(sample_task, i) for i in range(5)]
    
    print("Waiting for tasks to finish...")
    time.sleep(8)
    
    print(f"{'ID':<38} | {'State':<10} | {'Attempts':<8} | {'Result/Error'}")
    print("-" * 80)
    for t in tq.results():
        res = t['result'] if t['state'] == 'done' else t['error']
        print(f"{t['id']:<38} | {t['state']:<10} | {t['attempts']:<8} | {res}")