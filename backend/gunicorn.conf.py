from multiprocessing import cpu_count


def max_workers() -> int:
    return cpu_count() // 2 + 1


bind = "0.0.0.0:8000"
worker_class = "uvicorn.workers.UvicornWorker"
workers = max_workers()
