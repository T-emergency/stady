from django.utils import timezone
from study.utils import get_sub_time
# 일차적으로 프론트에서 페이지를 나갈 경우 종료를 시키는 함수가 존재하나 방어 코드를 대비
# 공부 인증을 마지막으로 페이지를 벗어나면 생기는 공부 지속
from study.models import StudyLog
def crontab_recent_check():
    
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