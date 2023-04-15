from config import *
from datetime import datetime

class IDatabaseHandler:
    def create_connection(self):
        pass

    def execute_query(self, query: str):
        pass
    
    def execute_table(self, table_name: str):
        pass
    
    def update(self, table_name: str, column: str, value: str, condition_column: str, condition_value: str):
        pass
    
    def insert(self, table_name: str, column: str, value: str):
        pass
    
    def close_connection(self):
        pass

class IListHandler:
    def update_list_of_lists_and_content_from_db(self):
        pass
    
    def get_list(self):
        pass
    
    def exist_in_list(self, name: str, key: str):
        pass
    
    def exist_in_list_by_time(self, name: str, key: str, date: datetime):
        pass