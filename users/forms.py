from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Account, Profile, Invite
from taggit.managers import TaggableManager
from taggit.forms import TagField, TagWidget


class AccountRegisterForm(UserCreationForm):
    CHOICES = [('is_employee','Employee'),('is_employer','Employer')]
    user_types = forms.CharField(label="User Type",widget=forms.RadioSelect(choices=CHOICES))

    class Meta:
        model = Account
        fields = ['email','first_name','last_name','birth_day','location']
        widgets = {
            'birth_day' : forms.DateInput(attrs={'type':'date'})
        }
        error_messages = {
            'email': {
                'required': 'Email is required',
                'invalid': 'Invalid email address'
            },
            'first_name': {
                'required': 'Please enter your Firstname'
            },
            'last_name': {
                'required': 'Please enter your lastname'
            },
            'birth_day': {
                'required': 'Please enter your birthday'
            },
            'birth_day': {
                'required': 'Enter your Location'
            },
            'password1': {
                'required': 'Password is required',
            },
            'password2': {
                'required': 'Confirm your password',
            },
        }

class AccountLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AccountLoginForm, self).__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = "Invalid email or password"
    class Meta:
        model = Account
        fields = ['email','password']


class UserUpdateForm(forms.ModelForm):
    skills = TagField(widget=TagWidget(attrs={'id': 'form-q'}), required=False)
    class Meta:
        model = Profile
        exclude = ('user',)
        fields = ['image','about','education','resume','website','github','twitter','instagram','company','skills']
        labels = {
            "image": "Update Profile Image",
            "resume": "Resume",
            "skills":"skills"
        }
        widgets = {
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'github': forms.URLInput(attrs={'class': 'form-control'})
        }

class InviteEmployeeForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ('date','message','is_selected','is_rejected')

        widgets = {
            'date':forms.DateInput(attrs={'type':'date'}),
            'message':forms.Textarea(attrs={'placeholder': 'Type message here','id':'msg-box'})
        }
 