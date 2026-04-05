import uuid
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Optional

class TaskQueue:
    def __init__(self, max_workers: int = 5):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()

    def submit(self, fn: Callable, *args: Any, **kwargs: Any) -> str:
        task_id = str(uuid.uuid4())
        with self.lock:
            self.tasks[task_id] = {
                "id": task_id,
                "state": "pending",
                "result": None,
                "attempts": 0,
                "error": None,
                "fn": fn,
                "args": args,
                "kwargs": kwargs
            }
        self.executor.submit(self._run_task_with_retry, task_id)
        return task_id

    def _run_task_with_retry(self, task_id: str) -> None:
        max_attempts = 3
        backoffs = [1, 2, 4]
        
        while True:
            with self.lock:
                task = self.tasks[task_id]
                task["attempts"] += 1
                attempt = task["attempts"]
                task["state"] = "running"
            
            try:
                # Execute the function
                res = task["fn"](*task["args"], **task["kwargs"])
                with self.lock:
                    task["result"] = res
                    task["state"] = "done"
                return
            except Exception as e:
                if attempt < max_attempts:
                    # Exponential backoff
                    time.sleep(backoffs[attempt-1])
                    continue
                else:
                    with self.lock:
                        task["error"] = str(e)
                        task["state"] = "failed"
                    return

    def status(self, task_id: str) -> Dict[str, Any]:
        with self.lock:
            if task_id not in self.tasks:
                return {}
            t = self.tasks[task_id]
            return {
                "id": t["id"],
                "state": t["state"],
                "result": t["result"],
                "attempts": t["attempts"],
                "error": t["error"]
            }

    def results(self) -> List[Dict[str, Any]]:
        with self.lock:
            return [self.status(tid) for tid in self.tasks]

def demo_task(n: int, fail: bool = False) -> str:
    if fail:
        raise RuntimeError(f"Simulated failure for task {n}")
    return f"Result of task {n}"

if __name__ == "__main__":
    tq = TaskQueue(max_workers=2)
    ids = []
    
    # Submit 5 tasks, 2 configured to fail
    for i in range(5):
        should_fail = i in (1, 3)
        tid = tq.submit(demo_task, i, fail=should_fail)
        ids.append(tid)
    
    # Wait and display status table
    print(f"{'TASK ID':<38} | {'STATE':<10} | {'ATTP':<4} | {'RESULT/ERROR'}")
    print("-" * 80)
    
    completed = set()
    while len(completed) < 5:
        for tid in ids:
            if tid in completed:
                continue
            s = tq.status(tid)
            if s["state"] in ("done", "failed"):
                res_err = s["result"] if s["state"] == "done" else s["error"]
                print(f"{tid:<38} | {s['state']:<10} | {s['attempts']:<4} | {res_err}")
                completed.add(tid)
        time.sleep(0.5)