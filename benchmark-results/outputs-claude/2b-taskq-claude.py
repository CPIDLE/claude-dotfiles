import threading
import time
import uuid
import random
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable


BACKOFF_SCHEDULE = [1, 2, 4]
MAX_ATTEMPTS = 3


class TaskQueue:
    """Thread-safe in-memory task queue with auto-retry and exponential backoff."""

    def __init__(self, max_workers: int = 4) -> None:
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._lock = threading.Lock()
        self._tasks: dict[str, dict[str, Any]] = {}

    def submit(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> str:
        """Submit a task. Returns a unique task ID."""
        task_id = str(uuid.uuid4())
        with self._lock:
            self._tasks[task_id] = {
                "id": task_id,
                "state": "pending",
                "result": None,
                "attempts": 0,
                "error": None,
            }
        self._executor.submit(self._run, task_id, fn, args, kwargs)
        return task_id

    def _run(self, task_id: str, fn: Callable, args: tuple, kwargs: dict) -> None:
        for attempt in range(MAX_ATTEMPTS):
            with self._lock:
                self._tasks[task_id]["state"] = "running"
                self._tasks[task_id]["attempts"] = attempt + 1

            try:
                result = fn(*args, **kwargs)
                with self._lock:
                    self._tasks[task_id]["state"] = "done"
                    self._tasks[task_id]["result"] = result
                return
            except Exception as exc:
                if attempt < MAX_ATTEMPTS - 1:
                    time.sleep(BACKOFF_SCHEDULE[attempt])
                else:
                    with self._lock:
                        self._tasks[task_id]["state"] = "failed"
                        self._tasks[task_id]["error"] = f"{type(exc).__name__}: {exc}"

    def status(self, task_id: str) -> dict[str, Any]:
        """Return status dict for a single task."""
        with self._lock:
            task = self._tasks.get(task_id)
            return task.copy() if task else {}

    def results(self) -> list[dict[str, Any]]:
        """Return status dicts for all tasks."""
        with self._lock:
            return [t.copy() for t in self._tasks.values()]


def main() -> None:
    """CLI demo: 5 tasks, 2 randomly fail."""
    tq = TaskQueue(max_workers=3)
    fail_indices = set(random.sample(range(5), 2))

    def work(i: int) -> str:
        time.sleep(0.3)
        if i in fail_indices:
            raise RuntimeError(f"task-{i} failed")
        return f"task-{i} ok"

    print(f"Submitting 5 tasks (failing: {sorted(fail_indices)})")
    ids = [tq.submit(work, i) for i in range(5)]

    while True:
        res = tq.results()
        if all(r["state"] in ("done", "failed") for r in res):
            break
        time.sleep(0.5)

    print(f"\n{'ID':<38} | {'State':<8} | {'Try'} | {'Result/Error'}")
    print("-" * 80)
    for r in res:
        msg = r["result"] if r["state"] == "done" else r["error"]
        print(f"{r['id']:<38} | {r['state']:<8} | {r['attempts']:<3} | {msg}")


if __name__ == "__main__":
    main()
