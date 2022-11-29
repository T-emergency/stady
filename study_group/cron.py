from datetime import date, timedelta
from study.models import StudyLog
from study_group.models import Study, Student
from user.models import User, UserProfile
from django.utils import timezone
from study.utils import get_sub_time
import random


def crontab_penalty_student():

    """
    벌금 체크 함수
    """

    weekday = timezone.now().today().weekday() - 1
    yesterday = (date.today() - timedelta(1)).strftime('%Y-%m-%d')
    penalty_studies = Study.objects.filter(is_penalty = True, days__contains = str(weekday))
    all_accept_student = Student.objects.filter(is_accept = True).exclude(join_dt = yesterday)
    all_today_study_logs = StudyLog.objects.filter(date = yesterday)
    update_students = []
    update_studies = []

    for study in penalty_studies:
        study_type = study.limit_type
        study_students = [student for student in all_accept_student if student.post == study]

        for student in study_students:
            is_penalty_student = False

            if study_type == "TT":
                total_time = sum([ get_sub_time(log.start_time, log.end_time) for log in all_today_study_logs.filter(user = student.user)])

                if total_time < study.limit_time:
                    is_penalty_student = True

            elif study_type == "CT":
                logs = all_today_study_logs.filter(user = student.user).order_by('start_time')

                if logs.exists():
                    
                    first_log_time = logs[0].start_time
                    first_log_time = first_log_time.hour

                    if first_log_time > study.limit_time:
                        is_penalty_student = True
                else:
                    is_penalty_student = True

            if is_penalty_student:
                #이렇게 쓰면 for문 돌 때마다 확인하나
                user_money = student.user.userprofile.money
                user_money -= study.penalty
                if user_money < 0 :
                    student.is_accept = False
                    update_students.append(student)
                    continue

                student.user.userprofile.money -= study.penalty
                student.week_penalty += study.penalty
                student.total_penalty += study.penalty
                study.total_penalty += study.penalty
                study.week_penalty += study.penalty

                update_students.append(student)
        update_studies.append(study)


    Study.objects.bulk_update(update_studies, ["week_penalty", "total_penalty"])
    Student.objects.bulk_update(update_students, ["week_penalty", "total_penalty"])
    

def crontab_week_penalty_reset():
    """
    한 주 마다의 벌금 리셋
    """
    penalty_studies = Study.objects.filter(is_penalty = True)
    all_accept_student = Student.objects.filter(is_accept = True)
    all_user = UserProfile.objects.all()

    stuies = []
    students = []
    users = []

    for user in all_user:
        user.money += 5000
        users.append(user)

    for study in penalty_studies:

        student = random.choice(study.student_set.all())
        student.user.userprofile.money += study.week_penalty
        students.append(student)

        study.week_penalty = 0
        stuies.append(study)

    for student in all_accept_student:
        student.week_penalty = 0
        students.append(student)

    UserProfile.objects.bulk_update(users, ['money'])
    Study.objects.bulk_update(stuies, ["week_penalty"])
    Student.objects.bulk_update(list(set(students)), ["week_penalty"])