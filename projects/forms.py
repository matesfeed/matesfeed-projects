from django.forms import ModelForm
from . import models

class ProjectForm(ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'title',
            'description',
            'link',
            'contact',
            'language'
        ]

class IssueForm(ModelForm):
    class Meta:
        model = models.Issue
        fields = [
            'issue_title',
        ]