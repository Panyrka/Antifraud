from database import DatabaseHandler
from config import ApplicationConfig
from datetime import datetime as dt, timedelta
from dateutil.relativedelta import relativedelta
import round_time
import decimal

# Следующая логика:
# 1. Подгруждаем все профили из БД
# 2. Проверяем, для всех ли профилей создана таблица
# 3. Если таблица не создана, то создаём
# 4. Готовы к работе

class Profile:
    def __init__(self, name: str, time_unit: str, time_unit_interval: int, code: str, db: DatabaseHandler):
        self.name = name
        self.time_unit = time_unit
        self.time_unit_interval = time_unit_interval
        self.code = code
        self.db = db
        
    def __str__(self):
        return f"Profile(name='{self.name}', time_unit='{self.time_unit}', time_unit_interval={self.time_unit_interval}, code='{self.code}')"
    
    def __round_date_time_profile_unit(self, datetime: dt):
        if self.time_unit == 'h':
            return round_time.round_to_hour(datetime)
        elif self.time_unit == 'd':
            return round_time.round_to_day(datetime)
        elif self.time_unit == 'm':
            return round_time.round_to_month(datetime)
        elif self.time_unit == 'y':
            return round_time.round_to_year(datetime)
        raise RuntimeError("Undefined time unit")
    
    def __time_delta(self, datetime: dt):
        if self.time_unit == 'h':
            return datetime - timedelta(hours=self.time_unit_interval)
        elif self.time_unit == 'd':
            return datetime - timedelta(days=self.time_unit_interval)
        elif self.time_unit == 'm':
            return datetime - relativedelta(months=self.time_unit_interval)
        elif self.time_unit == 'y':
            return datetime - relativedelta(years=self.time_unit_interval)
        raise RuntimeError("Undefined time unit")
    
    def __get_last_row_by_time(self, datetime: dt, key: str):
        query = f"SELECT amount FROM {self.name} WHERE date = '" + str(datetime) + "' and key = '" + key + "'"
        self.db.cur.execute(query)
        result = self.db.cur.fetchall()
        self.db.conn.commit()
        return result
    
    def __write(self, datetime: dt, amount: float, key: str):
        query = f"INSERT INTO " + self.name + " (amount, date, key) VALUES (" + str(amount) + ", '" + str(datetime) +"', '" + key + "');"
        self.db.cur.execute(query)
        self.db.conn.commit()
    
    def __update(self, datetime: dt, amount: float, key: str):
        query = f"UPDATE " + self.name  + " SET amount = " + str(amount) + " WHERE date = '" + str(datetime) + "' and key = '" + key + "';"
        self.db.cur.execute(query)
        self.db.conn.commit()
    
    def write(self, datetime: dt, amount: float, key: str):
        rounded = self.__round_date_time_profile_unit(datetime)
        last_value = self.__get_last_row_by_time(rounded, key)
        print(last_value)
        if last_value == []:
           # pass
            self.__write(rounded, amount, key)
        else:
           # pass
            value = (decimal.Decimal(amount) + decimal.Decimal(last_value[0][0]))
            self.__update(rounded, float(value), key)
    
    def get_sum(self, key: str, datetime: dt):
        rounded = self.__round_date_time_profile_unit(datetime)
        delta = self.__time_delta(rounded)
        query = f"SELECT SUM(amount) FROM {self.name} WHERE date >= '" + str(delta) + "' and key = '" + key + "'"
        self.db.cur.execute(query)
        result = self.db.cur.fetchall()
        self.db.conn.commit()
        return result
    
    def get_count(self, key: str, datetime: dt):
        rounded = self.__round_date_time_profile_unit(datetime)
        delta = self.__time_delta(rounded)
        query = f"SELECT COUNT(amount) FROM {self.name} WHERE date >= '" + str(delta) + "' and key = '" + key + "'"
        self.db.cur.execute(query)
        result = self.db.cur.fetchall()
        self.db.conn.commit()
        return result
    
class ProfilesHandler:
    def __init__(self, db: DatabaseHandler):
        self.table_name = 'profiles'
        self.db = db
        self.profiles = {}
    
    def __create_table_if_not_exists(self, table_name):
        create_table_query = 'CREATE TABLE IF NOT EXISTS ' + table_name + '''
        (
            id SERIAL PRIMARY KEY,
            key varchar(64),
            amount float8,
            date timestamp
        );
        '''
        self.db.cur.execute(create_table_query)
        self.db.conn.commit()
    
    def update(self):
        rows = self.db.execute_table(self.table_name)
        if rows == []:
            return
        
        for row in rows:
            profile = Profile(row[1], row[3], row[4], row[5], self.db)
            self.profiles[profile.name] = profile
            self.__create_table_if_not_exists(profile.name)
            
    def get_filters(self):
        filters = []
        for profile in self.profiles.values():
            filters.append({'name': profile.name, 'filter': profile.code})
        return filters
    
    def write(self, profile_name: str, amount: float, datetime: dt, key: str):
        if profile_name not in self.profiles:
            raise RuntimeError("Undefined profile name")
        profile = self.profiles[profile_name]
        profile.write(datetime, amount, key)

    def get_sum(self, profile_name: str, key: str, datetime: dt):    
        if profile_name not in self.profiles:
            raise RuntimeError("Undefined profile name")
        profile = self.profiles[profile_name]
        if profile.get_sum(key, datetime)[0][0] == None:
            return 0
        return profile.get_sum(key, datetime)[0][0]
    
    def get_count(self, profile_name: str, key: str, datetime: dt):
        if profile_name not in self.profiles:
            raise RuntimeError("Undefined profile name")
        profile = self.profiles[profile_name]
        if profile.get_count(key, datetime)[0][0] == None:
            return 0
        return profile.get_count(key, datetime)[0][0]

## import database
## import config
## 
## uc = config.UserConfig()
## db = database.DatabaseHandler(uc)
## db.create_connection();
## ph = ProfilesHandler(db)
## ph.update()
## #ph.write('ClientActivity_5d', 100, dt.now(), "5djn43045r3n")
## print(ph.get_sum('ClientActivity_5d', '5djn43045r3n', dt.now()))
## print(ph.get_count('ClientActivity_5d', '5djn43045r3n', dt.now()))