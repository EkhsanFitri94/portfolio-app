from django.contrib import admin
from .models import Project, Category, Tag, ProjectImage, Comment, Like

# Register your models here.
admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ProjectImage)
admin.site.register(Comment)
admin.site.register(Like)