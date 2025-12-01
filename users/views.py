from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from taggit.models import *
from jobs.models import Job
from .forms import AccountRegisterForm, UserUpdateForm, InviteEmployeeForm ,AccountLoginForm
# Create your views here.
from django.views.generic import CreateView, UpdateView, DetailView,ListView

from .models import Profile, Account, Invite


class UserRegisterView(SuccessMessageMixin,CreateView):
    template_name = 'users/user-register.html'
    form_class = AccountRegisterForm
    success_url = '/'
    success_message = "Your user account has been created!"


    def form_valid(self, form):
        user = form.save(commit=False)
        user_type = form.cleaned_data['user_types']
        if user_type == 'is_employee':
            user.is_employee = True
        elif user_type == 'is_employer':
            user.is_employer = True
        user.save()

        return redirect(self.success_url)

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = AccountLoginForm

class UserLogoutView(LogoutView):
    template_name = 'users/login.html'

@method_decorator(login_required(login_url='/users/login'),name='dispatch')
class UserUpdateView(SuccessMessageMixin,UpdateView):
    model = Profile
    success_message = "You updated your profile!"
    template_name = 'users/update.html'
    form_class = UserUpdateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserUpdateView, self).form_valid(form)

    def get(self,request,*args,**kwargs):
        profile = Profile.objects.filter(user_id=self.kwargs['pk'])
        print(f"{profile} user id in profile")
        return super(UserUpdateView, self).get(request,*args,**kwargs)

    def get_success_url(self):
        return reverse('users:my_profile',kwargs={'pk':self.object.pk})

class EmployeeProfileView(CreateView):
    template_name = 'users/employee-profile.html'
    model = Account
    form_class = InviteEmployeeForm

    def get_context_data(self, **kwargs):
        context = super(EmployeeProfileView, self).get_context_data(**kwargs)
        context['account'] = Account.objects.get(pk=self.kwargs['employee_id'])
        context['profile'] = Profile.objects.get(user_id=self.kwargs['employee_id'])
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        context['is_selected'] = Invite.objects.filter(user=self.kwargs['employee_id'],job=self.kwargs['job_id'],is_selected=True).exists()
        context['is_rejected'] = Invite.objects.filter(user=self.kwargs['employee_id'],job=self.kwargs['job_id'],is_rejected=True).exists()
        context['tags'] = Profile.objects.get(user_id=self.kwargs['employee_id']).skills.all() 
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = Account.objects.get(pk=self.kwargs['employee_id'])
        instance.job = Job.objects.get(pk=self.kwargs['job_id'])
        company = Job.objects.get(pk=self.kwargs['job_id']).company
        title = Job.objects.get(pk=self.kwargs['job_id']).title
        type = Job.objects.get(pk=self.kwargs['job_id']).job_type
        if self.request.POST.get('select', None):
            instance.is_selected = True
            instance.message = f"Thank you for applying for {title} with our company. We have reviewed your application and resume and are pleased to inform you that you have been selected to move forward in the hiring process. \n Thank you for considering this opportunity, and we hope to see you as a member of our team soon."
            instance.company = company
            instance.title = title
            instance.type = type
        elif self.request.POST.get('reject', None):     
            instance.is_rejected = True
            instance.message = f"Thank you for applying for {title} with our company. We appreciate the time and effort you put into submitting your application and resume. \n After careful review, we have decided to move forward with other candidates who are a better fit for the position. We apologize for any inconvenience this may cause and wish you the best of luck in your job search. \n Thank you again for considering our company and we hope you will keep us in mind for future opportunities."
            instance.company = company
            instance.title = title
            instance.type = type
        instance.save()
        return super(EmployeeProfileView, self).form_valid(form)

    def get_success_url(self):
        return reverse('users:employer_jobs')


class MyProfileView(DetailView):
    template_name = 'users/employee-profile.html'
    model = Account

    def get_context_data(self, **kwargs):
        context = super(MyProfileView, self).get_context_data(**kwargs)
        user = self.request.user
        context['account'] = user
        context['profile'] = user.profile
        context['tags'] = Profile.objects.get(user_id=self.kwargs['pk']).skills.all() 
        return context
         

@method_decorator(login_required(login_url='/users/login'),name='dispatch')
class EmployerPostedJobsView(ListView):
    template_name = 'users/employer-posted-jobs.html'
    context_object_name = 'employer_jobs'
    model = Job
    paginate_by = 3

    def get_queryset(self):
        return Job.objects.filter(employer=self.request.user).order_by('-id')


@method_decorator(login_required(login_url='/users/login'),name='dispatch')
class EmployeeMessagesView(ListView):
    model = Invite
    template_name = 'users/employee-messages.html'
    paginate_by = 5
    context_object_name = 'invites'

    def get_queryset(self):
        i = Invite.objects.filter(user_id=self.request.user).order_by('-id').values('id','title')
        return i

class EmployeeDisplayMessages(DetailView):
    model = Invite
    template_name = 'users/employee-display-messages.html'
    context_object_name = 'invite_message'

    def get_queryset(self):
        invite = self.model.objects.filter(id=self.kwargs['pk'])
        print(invite)
        invite.update(unread=False)
        return invite        

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        return super(EmployeeDisplayMessages, self).get(request,*args,**kwargs)

@method_decorator(login_required(login_url='/users/login'),name='dispatch')
class SaveJobView(UpdateView):
    template_name = 'jobs/index.html'
    model = Profile

    def get(self,request,*args,**kwargs):
        if self.request.user.is_employee:
            job = Job.objects.get(id=self.kwargs['pk'])
            profile = Profile.objects.get(user=request.user)
            profile.save_job.add(job)
            return redirect('jobs:home')

        else:
            return redirect('jobs:home')

@method_decorator(login_required(login_url='/users/login'),name='dispatch')
class RemoveFromSavedJobsView(UpdateView):
    template_name = 'jobs/index.html'
    model = Profile

    def get(self, request, *args, **kwargs):
        if self.request.user.is_employee:
            job = Job.objects.get(id=self.kwargs['pk'])
            profile = Profile.objects.get(user=request.user)
            profile.save_job.remove(job)
            return redirect('jobs:home')

        else:
            return redirect('jobs:home')

class MySavedJobsView(ListView):
    template_name = 'users/my-saved-jobs.html'
    context_object_name = 'jobs'
    model = Job
    paginate_by = 5

    def get_queryset(self):
        return Job.objects.filter(save_job__user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(MySavedJobsView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['save_job']=Job.objects.filter(save_job__user_id=self.request.user.id).values_list('id',flat=True)
        return context

        