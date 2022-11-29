from django.utils import timezone
from study.utils import get_sub_time
from study.models import StudyLog

def crontab_recent_check():
    """
    최근 인증 시간과 현재 시간을 체크하고 기준 시간 이상일 경우 공부로그 종료 함수
    """    
    not_end_log = StudyLog.objects.filter(end_time = None)
    studying_user = [log.user for log in not_end_log]
    fake_study_user = []

    for user, log in zip(studying_user, not_end_log):
        if (timezone.now() - user.recent_check).seconds >= 60 * 15:
            log.end_time = user.recent_check
            if get_sub_time(log.start_time, log.end_time) < 5:
                log.is_delete = True

            fake_study_user.append(log)
            

    StudyLog.objects.bulk_update(fake_study_user, ['end_time', 'is_delete'])

    StudyLog.objects.filter(is_delete = True).delete() # 5분 미만 삭제

    # django-bulk-update를 사용해야하나, []