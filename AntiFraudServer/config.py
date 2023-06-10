class UserConfig:
    DB_NAME = 'antifraud'
    DB_USER = 'postgres'
    DB_PASSWORD = 'password'
    logger_level = 10 # debug

class ApplicationConfig:
    platfrom_lists_table = 'platform_lists'
    profiles_table = 'profiles'
