import os


class SettingsError(Exception):
    pass


DB_ENV = ("sqlite", "postgresql")

def get_db_env():
    db_env = os.getenv("DB_ENV", "postgresql")
    if db_env not in DB_ENV:
        raise SettingsError(
            f"DB_ENV: {db_env} missing from config map. Known envs: {DB_ENV}"
        )
    print(f"Database environment: {db_env}")
    return db_env


def create_db_setup(config_map, db_env):
    try:
        db_setup = config_map[db_env]
    except KeyError as exc:
        raise SettingsError(
            f"DB_ENV: {db_setup} missing from config map. Know evns: {config_map.keys}"
        ) from exc
    return db_setup