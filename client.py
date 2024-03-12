from clickhouse_driver import Client


def get_client(host, port):
    return Client(host, port)