from config import ApplicationConfig, UserConfig
from datetime import datetime
from Interfaces import IListHandler, IDatabaseHandler
import logging

logging.basicConfig(level=UserConfig.logger_level)
logger = logging.getLogger('platform_lists')

class ListValue:
    def __init__(self, desc, valid, valid_from, valid_until):
        self.desc = desc
        self.valid = valid
        self.valid_from = valid_from
        self.valid_until = valid_until
        
    def __str__(self):
        return str([self.desc, self.valid, self.valid_from, self.valid_until])

class PlatformList:
    def __init__(self, name: str, db: IDatabaseHandler):
        self.name = name
        self.db = db
    
    def update_from_db(self):
        self.last_update = datetime.now()
        
        rows = self.db.execute_table(self.name)
        if rows != []:
            self.list_values = {}
            for row in rows:
                self.list_values[row[1]] = ListValue(row[2], row[3], row[4], row[5])
    
    def is_update_needed(self, last_db_update: datetime):
        if self.last_update is None:
            return True
        if self.last_update < last_db_update:
            return True
        return False
    
    def exist_in_list(self, key: str):
        value = self.list_values.get(key)
        if value is None:
            return False
        if value.valid:
            return True
        return False
    
    def exist_in_list_by_time(self, key: str, date: datetime):
        value = self.list_values.get(key)
        if value is None:
            return False
        if value.valid:
            if value.valid_until is None and value.valid_from is None:
                return True
            if date is not None and date >= value.valid_from and date <= value.valid_until:
                return True
        return False

class ListsHandler(IListHandler):
    def __init__(self, db: IDatabaseHandler, app_config: ApplicationConfig):
        self.db = db
        self.app_config = app_config
        self.lists = {}
        pass
    
    def update_list_of_lists_and_content_from_db(self):
        logger.debug('Started updating platform lists')
        rows = self.db.execute_table(self.app_config.platfrom_lists_table)
        for row in rows:
            name = row[1]
            pList = self.lists.get(name)
            if pList is None:
                self.lists[name] = PlatformList(name, self.db)
                self.lists[name].update_from_db()
                logger.debug('Create platform list ' + name)
            else:
                if pList.is_update_needed(row[2]):
                    self.lists[name] = PlatformList(name, self.db)
                    self.lists[name].update_from_db()
                    logger.debug('Updated platform list ' + name)
        logger.debug('Finished updating platform lists')
    
    def get_list(self):
        return self.lists
    
    def exist_in_list(self, name: str, key: str):
        return self.lists[name].exist_in_list(key)
    
    def exist_in_list_by_time(self, name: str, key: str, date: datetime):
        return self.lists[name].exist_in_list_by_time(key, date)