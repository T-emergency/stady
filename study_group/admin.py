from django.contrib import admin
from .models import Study, Student, Category

from study_group.models import Study

# Register your models here.
admin.site.register(Study)
admin.site.register(Student)
admin.site.register(Category)
