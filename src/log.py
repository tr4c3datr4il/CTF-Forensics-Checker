import logging
import os


logger = logging.getLogger("server_logger")
logger.setLevel(logging.INFO)

os.makedirs("logs", exist_ok=True)

handler = logging.FileHandler("logs/server.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def log_event(event_message):
    ip = get_connected_ip()
    if ip:
        logger.info(f"[{ip}] {event_message}")
    else:
        logger.info(event_message)

def get_connected_ip():
    return os.environ.get('CLIENT_IP', 'unknown')