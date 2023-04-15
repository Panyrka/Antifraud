from Interfaces import IDatabaseHandler
from config import ApplicationConfig
from datetime import datetime as dt
from round_time import *

class Profile:
    def __init__(self, name: str, date_segment: str, ds_number: int, filter):
        self.name = name
        self.date_segment = date_segment
        self.filter = filter
    
    def filter(self, transaction) -> bool:
        return self.filter(transaction)
    
    def get_current_date(self, d: dt):
        if self.date_segment == 'y':
            return round_to_year(d)
        elif self.date_segment == 'm':
            return round_to_month(d)
        elif self.date_segment == 'd':
            return round_to_day(d)
        elif self.date_segment == 'h':
            return round_to_hour(d)
        raise Exception('Undefined data segment type: ' + self.date_segment)

class ProfilesHandler:
    profiles: dict[str, Profile]
    
    def __init__(self, db: IDatabaseHandler, config: ApplicationConfig):
        self.db = db
        self.config = config
    
    def fetch_profiles_from_db(self):
        rows = self.db.execute_table(self.config.profiles_table)
        for row in rows:
            name = row[1]
            self.profiles[name] = Profile(name, row[2], row[3], None)
    
    def get_query_profile_fetch(self, name, key):
        return 'SELECT * FROM ' + name + ' WHERE key = \'' + key + '\''
    
    def get_query_current_ds_exist(self, name):
        return 'SELECT max(date_segment) from ' + name;
    
    def get_query_update_profilie(self, name: str, key: str, amount: int):
        return 'UPDATE ' + name + ' SET amount = ' + str(amount) + ' WHERE key = \'' + key + '\''
    
    def get_query_insert_profilie(self, name: str, key: str, amount: int):
        return 'INSERT INTO ' + name + ' (key, amount, date_segment) VALUES (\'' + str(key) + '\', ' + 
    
    def profile_fetch(self, name: str, key: str, date: dt):
        profile = self.profiles.get(name)
        if profile is None:
            raise Exception('No such profile: ' + name)
        
        query = self.get_query_profile_fetch(name, key)
        rows = self.db.execute_query(query)
        return rows
    
    def write(self, transaction):
        for profile in self.profiles.values():
            if profile.filter(transaction):
                last_date_query = self.get_query_current_ds_exist(profile.name)
                last_date = self.db.execute_query(last_date_query)
                curr_round_date = profile.get_current_date(transaction.normalizedDatetime)
                if last_date == curr_round_date:
                    
                    pass
                else:
                    # insert
                    pass                    
            
####

import database
import config

uc = config.UserConfig()
ac = config.ApplicationConfig()
db = database.DatabaseHandler(uc)
db.create_connection()

ph = ProfilesHandler(db, ac)
ph.fetch_profiles_from_db()