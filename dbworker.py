import json
import config

def get_current_state(user_id):
    with open(config.db_file) as db:
        try:
            return db[user_id]
        except KeyError:
            pass