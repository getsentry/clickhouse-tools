import sys
import waiting
import click
import logging
import requests

DEFAULT_TIMEOUT_THRESHOLD = 300
DEFAULT_POLL_PERIOD = 60

logging.basicConfig()
logger = logging.getLogger("replication_queue")
logger.setLevel(logging.INFO)


def _is_replication_queue_empty(host: str, port: str):
    response = requests.post(
        url=f"http://{host}:{port}",
        params={"query": "SELECT * FROM system.replication_queue"}
    )
    return len(response.text.strip()) == 0


@click.command()
@click.option("--host")
@click.option("--port")
@click.option("--timeout", default=DEFAULT_TIMEOUT_THRESHOLD)
@click.option("--poll", default=DEFAULT_POLL_PERIOD)
def check_replication_queue(host: str, port: str, timeout: int, poll: int):
    try:
        waiting.wait(lambda: _is_replication_queue_empty(host, port), sleep_seconds=poll, timeout_seconds=timeout)
    except waiting.TimeoutExpired:
        logger.error("Replication queue still non-empty at the end of %s seconds" % timeout)
        sys.exit(1)
    else:
        logger.info("Replication queue is empty")
        sys.exit(0)

if __name__ == '__main__':
    check_replication_queue()
