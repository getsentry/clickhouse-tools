from client import get_client
import sys
import waiting
import click
import logging


SNUBA_ADMIN_HOST = "127.0.0.1"
CLICKHOUSE_CLIENT_PORT = "9000"
DEFAULT_TIMEOUT_THRESHOLD = 300
DEFAULT_POLL_PERIOD = 60

logging.basicConfig()
logger = logging.getLogger("replication_queue")
logger.setLevel(logging.INFO)


def _is_replication_queue_empty(client):
    return len(client.execute("SELECT COUNT(*) FROM system.replication_queue LIMIT 1;")) == 0


@click.command()
@click.option("--host", default=SNUBA_ADMIN_HOST)
@click.option("--timeout", default=DEFAULT_TIMEOUT_THRESHOLD)
@click.option("--poll", default=DEFAULT_POLL_PERIOD)
def check_replication_queue(host: str, timeout: int, poll: int):
    client = get_client(host, CLICKHOUSE_CLIENT_PORT)
    try:
        waiting.wait(lambda: _is_replication_queue_empty(client), sleep_seconds=poll, timeout_seconds=timeout)
    except waiting.TimeoutExpired:
        client.disconnect()
        logger.error("Replication queue still non-empty at the end of %s seconds" % timeout)
        sys.exit(1)
    else:
        client.disconnect()
        logger.info("Replication queue is empty")
        sys.exit(0)
        


if __name__ == '__main__':
    check_replication_queue()
