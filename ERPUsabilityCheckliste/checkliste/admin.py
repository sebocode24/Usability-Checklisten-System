from django.contrib import admin
from .models import *

admin.site.register(Project)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Criterion)

