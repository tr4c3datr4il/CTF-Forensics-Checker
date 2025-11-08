import logging
import os


logger = logging.getLogger("server_logger")
logger.setLevel(logging.INFO)

os.makedirs("logs", exist_ok=True)

# setup file handler for logging
log_file = open("logs/server.log", "a", encoding="utf-8", errors="replace")
log_handler = logging.StreamHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

# sanitize input to ensure valid UTF-8
def _sanitize(obj):
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="backslashreplace")

    return obj.encode("utf-8", errors="backslashreplace").decode("utf-8")

def log_event(event_message):
    ip = get_connected_ip()
    msg = _sanitize(event_message)

    if ip:
        logger.info(f"[{ip}] {msg}")
    else:
        logger.info(msg)

def get_connected_ip():
    return os.environ.get('CLIENT_IP', 'unknown')