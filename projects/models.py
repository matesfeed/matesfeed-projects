from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from multiselectfield import MultiSelectField


# Create your models here.
PROJECT_LANGUAGES = [
        ('web', "Web Development"),
        ('cpp', "C plus plus"),
        ('ml', "Machine Learning"),
        ('ai', "Artificial Learning"),
        ('dl', "Deep Learning"),
        ('nn', "Neural Networks")
    ]

class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    language = MultiSelectField(
        choices=PROJECT_LANGUAGES,
        null=True
        )
    link = models.URLField(blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    developers_list = ArrayField(
            ArrayField(
                models.CharField(max_length=50), 
            ),
            default=list, 
            null=True
        )
    requests_list = ArrayField(
            ArrayField(
                models.CharField(max_length=50), 
            ),
            default=list, 
            null=True
        )
    ignored_list = ArrayField(
            ArrayField(
                models.CharField(max_length=50), 
            ),
            default=list,
            null=True
        )
    rejected_list = ArrayField(
            ArrayField(
                models.CharField(max_length=50), 
            ),
            default=list,
            null=True
        )
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    developers_requested = ArrayField(models.IntegerField(), default=list, null=True)
    developers_request_accepted = ArrayField(models.IntegerField(), default=list, null=True)
    developers_request_rejected = ArrayField(models.IntegerField(), default=list, null=True)
    project_resources = ArrayField(models.IntegerField(), default=list, null=True)

    def __str__(self):
        return self.title


class Issue(models.Model):
    issue_title = models.CharField(max_length=150)
    status = models.IntegerField()
    project_id = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    developers_list = ArrayField(models.IntegerField(), default=list, null=True)
    
    def __str__(self):
        return self.issue_title
