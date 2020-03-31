from django.forms import ModelForm
from django.contrib.auth.models import User
from . import models

class ProfileForm(ModelForm):
    class Meta: 
        model = models.Profile
        fields = [
            'first_name',
            'last_name',
            'interests',
            'bio',
        ] 
    