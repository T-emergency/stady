from django.shortcuts import get_object_or_404, redirect, render
from numpy import require
from .models import Study
# from django.contrib.auth.decorators import require_POST



# Create your views here.

def index(request): #인자는request
    study_list = Study.objects.all()
    context = {'study_list': study_list}
    return render(request, 'study_group/study_index.html', context)    

def study_detail(request, study_id):
    study = Study.objects.get(id=study_id)
    context={
        'study':study,
    }
    return render(request,'study_group/study_detail.html', context)        

def like(request, study_id):
    # 스터디 id에 해당하는 객체를 가져온다
    study = get_object_or_404(Study, pk=study_id)
    # 요청한 사용자
    user = request.user

    # 가져온 스터디의 객체에서 like에 가면 좋아요한 user있을건데(테이블이 있을거임)
    # 요청한 유저가 있는걸 filter함 그럼 필터말고 겟도 가능하지않나?
    filtered_like_study = study.like.filter(id=user.id)

    # 변수를 이용해서 존재할경우, study like 에서 유저 제거 해당 객체를 삭제한다고 이해함
    if filtered_like_study.exists():
        study.like.remove(user) #여기서 user는 뭘 의미하는지 모르겠네 아마 유저인듯
        return redirect('study_detail', study_id=study.id)

    # 없을 경우, study 객체에서 like에 해당 user를 추가
    else:
        study.like.add(user)
        return redirect('study_detail', study_id=study.id)

def submit(request, study_id):
    user=request.user
    study=get_object_or_404(Study, pk=study_id)
    filter_submit_study= study.submit.filter(id=user.id)
    if filter_submit_study.exists():
        study.submit.remove(user)
        return redirect('study_detail', study_id=study.id)
    else:
        study.submit.add(user)
        return redirect('study_detail', study_id=study.id)