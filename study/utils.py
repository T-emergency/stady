from datetime import datetime


def get_now_time(time):
    if time == None:
        return '현재'
    else:
        return time.strftime("%H:%M")


def get_sub_time(start_time, end_time):
    
    if end_time ==  None:
        return int((datetime.now() - start_time).total_seconds()//60)
    return int((end_time - start_time).total_seconds()//60)