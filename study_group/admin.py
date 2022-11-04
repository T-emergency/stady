from django.contrib import admin
from .models import Study, Student

from study_group.models import Study, Tag

# Register your models here.
admin.site.register(Study)
admin.site.register(Student)
admin.site.register(Tag)
