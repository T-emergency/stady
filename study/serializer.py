import json

# utils
from . import utils

def log_to_json(logs):
    log_list = []

    for log in logs:
        log_dict = {
            'id' : log.id,
            'start_time' : utils.get_now_time(log.start_time),
            'end_time' : utils.get_now_time(log.end_time),
            'memo' : log.memo,
            'date' : log.date,
            'sub_time': utils.get_sub_time(log.start_time, log.end_time)
        }

        log_list.append(log_dict)

    return log_list