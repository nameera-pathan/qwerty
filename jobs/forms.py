from django import forms
from .models import *
from taggit.managers import TaggableManager
from taggit.forms import TagField, TagWidget


class CreateJobForm(forms.ModelForm):
    salary = forms.DecimalField(max_digits=12, decimal_places=2, initial=0.00)
    class Meta:
        model = Job
        fields = ['title','company','location','job_type','description','companylogo','qualification','salary']
        labels = {
            "qualification": "Qualification"
        }
        widgets = {
            'job_type': forms.RadioSelect,
            'description': forms.Textarea(attrs={'id':'form-desc'}),
            'qualification': forms.TextInput(attrs={'id':'form-q'}),
        }
class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = []

class UpdateJobForm(forms.ModelForm):
    skills = TagField(widget=TagWidget(attrs={'id': 'form-q'}), required=False)
    class Meta:
        model = Job
        fields = ['title','company','location','job_type','description','companylogo','salary','skills','qualification','website','twitter','instagram','facebook']
        labels = {
            "companylogo": "Update Company Image",
            "qualification": "Qualification",
            "salary":"Salary",
            "skills":"Required Skills"
        }
        widgets = {
            'job_type': forms.RadioSelect,
            'description': forms.Textarea(attrs={'id':'form-desc'}),
            'qualification': forms.TextInput(attrs={'id':'form-q'}),
            'website': forms.TextInput(attrs={'id':'form-q'}),
            'twitter': forms.TextInput(attrs={'id':'form-q'}),
            'instagram': forms.TextInput(attrs={'id':'form-q'}),
            'facebook': forms.TextInput(attrs={'id':'form-q'}),
        }

