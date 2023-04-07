import psycopg2
from config import UserConfig
import logging

logging.basicConfig(level=UserConfig.logger_level)
logger = logging.getLogger('database')

class DatabaseHandler:
    def __init__(self, config: UserConfig):
        self.config = config
    
    def create_connection(self):
        self.conn = psycopg2.connect(
            dbname=self.config.DB_NAME,
            user=self.config.DB_USER,
            password=self.config.DB_PASSWORD
        )
        self.cur = self.conn.cursor()
        logger.info('Connected to database')

    def execute_query(self, query: str):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows
    
    def execute_table(self, table_name: str):
        self.cur.execute("SELECT * FROM " + table_name)
        rows = self.cur.fetchall()
        return rows
    
    def close_connection(self):
        self.cur.close()
        self.conn.close()
        logger.info('Disonnected from database')