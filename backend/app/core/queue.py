import asyncio
import uuid
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class TaskQueue:
    def __init__(self):
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._queue: asyncio.Queue = asyncio.Queue()
        self._is_running = False
        self._worker_task: Optional[asyncio.Task] = None

    async def enqueue(self, name: str, payload: Dict[str, Any] = None) -> str:
        task_id = f"task-{uuid.uuid4().hex[:8]}"
        task_record = {
            "id": task_id,
            "name": name,
            "status": "QUEUED",
            "payload": payload or {},
            "queued_at": datetime.now(timezone.utc).isoformat(),
            "started_at": None,
            "completed_at": None,
            "duration_ms": 0,
            "error": None
        }
        self._tasks[task_id] = task_record
        await self._queue.put(task_id)
        return task_id

    async def start_worker(self):
        self._is_running = True
        self._worker_task = asyncio.create_task(self._process_queue())

    async def stop_worker(self):
        self._is_running = False
        if self._worker_task:
            self._worker_task.cancel()

    async def _process_queue(self):
        while self._is_running:
            try:
                task_id = await self._queue.get()
                if task_id not in self._tasks:
                    self._queue.task_done()
                    continue

                task = self._tasks[task_id]
                task["status"] = "PROCESSING"
                task["started_at"] = datetime.now(timezone.utc).isoformat()
                t0 = time.time()

                # Simulate work processing
                await asyncio.sleep(0.3)

                task["duration_ms"] = round((time.time() - t0) * 1000, 1)
                task["status"] = "COMPLETED"
                task["completed_at"] = datetime.now(timezone.utc).isoformat()
                self._queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                if task_id in self._tasks:
                    self._tasks[task_id]["status"] = "FAILED"
                    self._tasks[task_id]["error"] = str(e)

    def get_stats(self) -> dict:
        tasks = list(self._tasks.values())
        queued = sum(1 for t in tasks if t["status"] == "QUEUED")
        processing = sum(1 for t in tasks if t["status"] == "PROCESSING")
        completed = sum(1 for t in tasks if t["status"] == "COMPLETED")
        failed = sum(1 for t in tasks if t["status"] == "FAILED")
        avg_latency = (
            sum(t["duration_ms"] for t in tasks if t["duration_ms"] > 0) / max(1, completed)
        )
        return {
            "total_tasks": len(tasks),
            "queued": queued,
            "processing": processing,
            "completed": completed,
            "failed": failed,
            "avg_duration_ms": round(avg_latency, 1),
            "is_worker_active": self._is_running
        }

    def get_recent_tasks(self, limit: int = 10) -> List[Dict[str, Any]]:
        tasks = list(self._tasks.values())
        tasks.sort(key=lambda x: x["queued_at"], reverse=True)
        return tasks[:limit]

    async def retry_failed(self) -> int:
        retried = 0
        for task in self._tasks.values():
            if task["status"] == "FAILED":
                task["status"] = "QUEUED"
                task["error"] = None
                await self._queue.put(task["id"])
                retried += 1
        return retried

app_queue = TaskQueue()
