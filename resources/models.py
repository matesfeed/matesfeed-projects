from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from projects.models import PROJECT_LANGUAGES
from django.contrib.postgres.fields import ArrayField
# Create your models here.
USER_LEVEL = [
    ("Beginner", "Beginner"),
    ("Intermediate", "Intermediate"),
    ("Advanced", "Advanced")
]

class Resource(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    tag = MultiSelectField(choices=PROJECT_LANGUAGES)
    link = models.URLField(null=True)
    user_level = models.CharField(max_length=15, choices=USER_LEVEL)
    img_src = models.URLField(null=True)
    description = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    projects_attached = ArrayField(models.IntegerField(), default=list, null=True)
    
    def __str__(self):
        return self.title