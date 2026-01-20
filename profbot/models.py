from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

# 1. The Assignment (Created by Teacher)
class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # The Rubric is crucial for Gemini to know HOW to grade
    rubric = models.TextField(help_text="Paste the grading criteria here")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 2. The Student's Submission
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100, default="Student") # Simplified for now
    
    # This stores the actual file (PDF or Image)
    answer_file = models.FileField(upload_to='submissions/')
    
    # We store AI results here so we don't have to pay for API calls twice
    ai_feedback = models.TextField(blank=True, null=True)
    marks_obtained = models.CharField(max_length=10, blank=True, null=True)
    
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.assignment.title}"