from django.forms import ModelForm
from . import models

class ResourceForm(ModelForm):
    class Meta:
        model = models.Resource
        fields = [
            'tag',
            'link',
            'user_level',
        ]