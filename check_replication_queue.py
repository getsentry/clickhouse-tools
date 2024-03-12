from client import get_client
import sys
import waiting
import click


SNUBA_ADMIN_HOST = "127.0.0.1"
CLICKHOUSE_CLIENT_PORT = "9000"

def _is_replication_queue_empty(client):
    return len(client.execute("SELECT * FROM system.replication_queue LIMIT 1;")) == 0


@click.command()
@click.option("--host", default=SNUBA_ADMIN_HOST)
def check_replication_queue(host: str):
    client = get_client(host, CLICKHOUSE_CLIENT_PORT)
    try:
        waiting.wait(lambda: _is_replication_queue_empty(client), sleep_seconds=60, timeout_seconds=300)
    except waiting.TimeoutExpired as e:
        client.disconnect()
        print(e)
        sys.exit(1)
    else:
        client.disconnect()
        print("replication queue is empty")
        sys.exit(0)
        


if __name__ == '__main__':
    check_replication_queue()
