import multiprocessing
import os

print(f"ENVIRONMENT {os.environ.get('ENVIRONMENT')}")
if os.environ.get("ENVIRONMENT") == "development":
    workers = multiprocessing.cpu_count()  # or 1
    # workers = 1
    # reload = True
else:
    workers = multiprocessing.cpu_count()
    # workers = 1

print(f"Report API - Num Workers: {workers}")
print(f"Report API - v.1.0")

bind = "0.0.0.0:8001"
keepalive = 120
errorlog = "-"
pidfile = "/tmp/fastapi.pid"
loglevel = "info"
accesslog = "-"
