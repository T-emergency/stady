from django.contrib import admin
from .models import Study, Student, Category

from study_group.models import Study, Tag

admin.site.register(Study)
admin.site.register(Student)
admin.site.register(Tag)
admin.site.register(Category)
