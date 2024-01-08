import snowflake.connector
from snowflake.connector.connection import SnowflakeConnection as SFConnection
from . import logger
from .models import SnowFlakeConnection


class SnowFlake(object):

    def __init__(self, connection_id: int, external: bool = False) -> None:
        connection: SnowFlakeConnection = SnowFlakeConnection.query.filter_by(
            connection_name=connection_id).first()
        self.connection = connection

    def connect(self) -> SFConnection:
        connection_name = self.identifier
        logger.info(f"Attempting to connect snowflake {connection_name=}")
        username = self.username
        password = self.password
        account = self.account
        proxyhost = self.proxyhost
        proxyport = self.proxyport
        if proxyhost is None or proxyhost.strip() == "":
            con = snowflake.connector.connect(
                user=username, password=password, account=account)
        else:
            con = snowflake.connector.connect(
                user=username, password=password, account=account, proxy_host=proxyhost, proxy_port=proxyport)
        logger.info("SnowFlake DB Connected")
        self.connection: SFConnection = con
        return con

    def get_database_list(self) -> list:
        cursor = self.connection.cursor()
        if self.warehouse is not None and self.warehouse != "":
            cursor.execute(f"USE WAREHOUSE {self.warehouse}")

        cursor.execute("SHOW DATABASES")
        df = self.get_data_from_cursor(cursor)
        database_list = df['name'].tolist()
        return database_list
