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


def _is_replication_delay_acceptable(host: str, port: str, allowed_delay: int):
    response = requests.post(
        url=f"http://{host}:{port}",
        params={"query": "SELECT value FROM system.asynchronous_metrics where metric = 'ReplicasMaxAbsoluteDelay'"}
    )
    return response.text.strip() <= allowed_delay


@click.command()
@click.option("--host")
@click.option("--port")
@click.option("--delay")
@click.option("--timeout", default=DEFAULT_TIMEOUT_THRESHOLD)
@click.option("--poll", default=DEFAULT_POLL_PERIOD)
def replication_delay(host: str, port: str, delay: int, timeout: int, poll: int):
    try:
        waiting.wait(lambda: _is_replication_delay_acceptable(host, port, delay), sleep_seconds=poll, timeout_seconds=timeout)
    except waiting.TimeoutExpired:
        logger.error("Replication delay is still greater than %s seconds at the end of %s seconds" % (delay, timeout))
        sys.exit(1)
    else:
        logger.info("Replication delay is under %s seconds" % delay)
        sys.exit(0)

