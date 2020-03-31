from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from multiselectfield import MultiSelectField
from projects.models import PROJECT_LANGUAGES
                                                    
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    interests = MultiSelectField(choices=PROJECT_LANGUAGES)
    projects_completed = ArrayField(models.IntegerField(), default=list, null=True)
    projects_working = ArrayField(models.IntegerField(), default=list, null=True)
    projects_requested = ArrayField(models.IntegerField(), default=list, null=True)
    project_requests_inbox = ArrayField(models.IntegerField(), default=list, null=True)
    projects_rejected = ArrayField(models.IntegerField(), default=list, null=True)
    projects_restarted = ArrayField(models.IntegerField(), default=list, null=True)
    projects_created = ArrayField(models.IntegerField(), default=list, null=True)
    projects_bookmarked = ArrayField(models.IntegerField(), default=list, null=True)
    resources_added = ArrayField(models.IntegerField(), default=list, null=True)
    resources_bookmarked = ArrayField(models.IntegerField(), default=list, null=True)
    dev_requests_inbox = ArrayField(models.IntegerField(), default=list, null=True)
    dev_requests_sent = ArrayField(models.IntegerField(), default=list, null=True)
    devs_connected = ArrayField(models.IntegerField(), default=list, null=True)

    def __str__(self):
        return self.user.username 
