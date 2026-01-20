from django.contrib import admin
from .models import Assignment, Submission

# This tells the Admin panel: "Please show these tables!"
admin.site.register(Assignment)
admin.site.register(Submission)