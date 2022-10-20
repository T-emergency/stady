
from django.utils import timezone

from datetime import datetime


def get_now_time(time):
    if time == None:
        return '현재'
    else:
        return time.strftime("%H:%M")
    

def get_sub_time(start_time, end_time):
    print('시작시간:',start_time)
    print('종료시간:',end_time)
    if end_time ==  None:
        print('end_time 없음')
        print(datetime.now())
        print(timezone.now())
        return int((datetime.now() - start_time).total_seconds()//60)
    # print(int((end_time - start_time).total_seconds()//60),'분')
    return int((end_time - start_time).total_seconds()//60)