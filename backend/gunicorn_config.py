import os

workers = max(0, int(os.getenv("WORKERS", "0"))) or ((os.cpu_count() or 1) * 4 + 1)

bind = "0.0.0.0:80"
