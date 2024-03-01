from django import forms
from .models import *

class TimeInput(forms.TimeInput):
    input_type = 'time'
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'shift':TimeInput()
        }
        exclude = ['present','updated', 'st']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        # self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['shift'].widget.attrs['class'] = 'form-control'