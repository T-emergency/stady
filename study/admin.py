from django.contrib import admin
from .models import StudyLog, InStudy, OutStudy


admin.site.register(StudyLog)
admin.site.register(InStudy)
admin.site.register(OutStudy)
