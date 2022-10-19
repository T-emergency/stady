

def get_now_time(time):
    if time == None:
        return '현재'
    else:
        return time.strftime("%H:%M")