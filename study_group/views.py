from django.shortcuts import render
from .models import Study
from django.http import HttpResponse

def create_study(request):
    if request.method == 'GET':
        return render(request, 'study_group/create.html')

    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title')
        thumbnail_img = request.FILES.get('image')
        headcount = request.POST.get('headcount')
        content = request.POST.get('content')

        Study.objects.create(title=title,thumbnail_img=thumbnail_img,headcount=headcount,content=content)

        # study = Study()
        # study.title = title
        # study.title = title
        # study.thumbnail_img = thumbnail_img
        # study.headcount = headcount
        # study.content = content
        # study.save()
        return HttpResponse('등록완료')
        
def studies(request):
        if request.method == 'GET':
            
            studys = Study.objects.all()
            content={
                "studys":studys
            }
        return render(request, 'study_group/studies.html',content)
