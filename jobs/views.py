from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from users.models import Account,Profile,Invite
from .models import Job
# Create your views here.
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView,DeleteView
from .forms import *
from taggit.models import Tag

class HomeView(ListView):
    template_name = 'jobs/index.html'
    context_object_name = 'jobs'
    model = Job
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['all_jobs'] = Job.objects.all().count() * 1997
        context['candidates']=Account.objects.filter(is_employee=True).count() * 2555
        context['resumes'] = Profile.objects.exclude(resume="").count() * 4779
        context['employers']= Account.objects.filter(is_employer=True).count() * 5235
        if self.request.user.is_authenticated:
            context['save_job']=Job.objects.filter(save_job__user_id=self.request.user.id).values_list('id',flat=True)
        return context


@method_decorator(login_required(login_url='/'),name='dispatch')
class CreateJobView(SuccessMessageMixin,CreateView):
    model = Job
    template_name = 'jobs/create-jobs.html'
    form_class = CreateJobForm
    success_url = '/'
    success_message = "Job has been posted!"
    
    def form_valid(self, form):
        job = form.save(commit=False)
        job.employer = self.request.user
        job.save()
        return super(CreateJobView, self).form_valid(form)


class SingleJobView(SuccessMessageMixin,UpdateView):
    template_name = 'jobs/single.html'
    model = Job
    context_object_name = 'job'
    form_class = ApplyJobForm
    success_message = "You applied this job!"

    def get_context_data(self, **kwargs):
        context = super(SingleJobView, self).get_context_data(**kwargs)
        context['employee_applied']=Job.objects.get(pk=self.kwargs['pk']).employee.all().filter(id=self.request.user.id)
        context['in_my_list'] = Job.objects.get(pk=self.kwargs['pk']).save_job.all().filter(user_id=self.request.user.id)
        context['tags'] = Job.objects.get(pk=self.kwargs['pk']).skills.all() 
        try:       
            context['employer_id'] = Job.objects.get(pk=self.kwargs['pk']).employer_id
            context['tags'] = Job.objects.get(pk=self.kwargs['pk']).skills.all() 
        except:
            pass
        return context
    
    
    def form_valid(self, form):
        employee = self.request.user
        form.instance.employee.add(employee)
        form.save()
        return super(SingleJobView, self).form_valid(form)

    def get_success_url(self):
        return reverse('jobs:single_job',kwargs={'slug':self.object.slug,"pk":self.object.pk})



class AppliedEmployeesView(SuccessMessageMixin,ListView):
    template_name = 'jobs/applied-employees.html'
    model = Job
    context_object_name = 'job'
    form_class = ApplyJobForm
    success_message = "You applied this job!"

    def get_context_data(self, **kwargs):
        context = super(AppliedEmployeesView, self).get_context_data(**kwargs)
        context['employee_applied']=Job.objects.get(pk=self.kwargs['pk']).employee.all().filter(id=self.request.user.id)
        all_applied_employees = Job.objects.get(pk=self.kwargs['pk'], employer_id=self.request.user.id).employee.all()
        rejected_employees = [employee for employee in all_applied_employees if Invite.objects.filter(user=employee, job_id=self.kwargs['pk'], is_rejected=True).exists()]
        selected_employees = [employee for employee in all_applied_employees if Invite.objects.filter(user=employee, job_id=self.kwargs['pk'], is_selected=True).exists()]
        applied_employees = [employee for employee in all_applied_employees if employee not in rejected_employees and employee not in selected_employees]
        context['applied_employees'] =  applied_employees
        context['employer_id'] = Job.objects.get(pk=self.kwargs['pk']).employer_id
        context['job_id'] = Job.objects.get(pk=self.kwargs['pk']).id
        return context
 
class SelectedEmployeesView(SuccessMessageMixin,ListView):
    template_name = 'jobs/selected-employees.html'
    model = Job
    context_object_name = 'job'
    form_class = ApplyJobForm
    success_message = "You applied this job!"

    def get_context_data(self, **kwargs):
        context = super(SelectedEmployeesView, self).get_context_data(**kwargs)
        context['employee_applied']=Job.objects.get(pk=self.kwargs['pk']).employee.all().filter(id=self.request.user.id)
        all_applied_employees = Job.objects.get(pk=self.kwargs['pk'], employer_id=self.request.user.id).employee.all()
        rejected_employees = [employee for employee in all_applied_employees if Invite.objects.filter(user=employee, job_id=self.kwargs['pk'], is_rejected=True).exists()]
        selected_employees = [employee for employee in all_applied_employees if Invite.objects.filter(user=employee, job_id=self.kwargs['pk'], is_selected=True).exists()]
        applied_employees = [employee for employee in all_applied_employees if employee not in rejected_employees and employee not in selected_employees]
        context['selected_employees'] = selected_employees
        context['employer_id'] = Job.objects.get(pk=self.kwargs['pk']).employer_id
        context['job_id'] = Job.objects.get(pk=self.kwargs['pk']).id
        return context

class RejectedEmployeesView(SuccessMessageMixin,ListView):
    template_name = 'jobs/rejected-employees.html'
    model = Job
    context_object_name = 'job'
    form_class = ApplyJobForm
    success_message = "You applied this job!"

    def get_context_data(self, **kwargs):
        context = super(RejectedEmployeesView, self).get_context_data(**kwargs)
        context['employee_applied']=Job.objects.get(pk=self.kwargs['pk']).employee.all().filter(id=self.request.user.id)
        all_applied_employees = Job.objects.get(pk=self.kwargs['pk'], employer_id=self.request.user.id).employee.all()
        rejected_employees = [employee for employee in all_applied_employees if Invite.objects.filter(user=employee, job_id=self.kwargs['pk'], is_rejected=True).exists()]
        selected_employees = [employee for employee in all_applied_employees if Invite.objects.filter(user=employee, job_id=self.kwargs['pk'], is_selected=True).exists()]
        applied_employees = [employee for employee in all_applied_employees if employee not in rejected_employees and employee not in selected_employees]
        context['rejected_employees'] = rejected_employees
        context['employer_id'] = Job.objects.get(pk=self.kwargs['pk']).employer_id
        context['job_id'] = Job.objects.get(pk=self.kwargs['pk']).id
        return context


class SearchJobView(ListView):
    model = Job
    template_name = 'jobs/search.html'
    paginate_by = 2
    context_object_name = 'jobs'

    def get_queryset(self):
        q1 = self.request.GET.get("job_title")
        q2 = self.request.GET.get("job_type")
        q3 = self.request.GET.get("job_location")

        if q1 or q2 or q3 :
            return Job.objects.filter(Q(title__icontains=q1)|
                                      Q(description__icontains=q1),
                                      job_type=q2,
                                      location__icontains=q3
                                      ).order_by('-id')
        return Job.objects.all().order_by('-id')

    def get_context_data(self, *args, **kwargs):
        context = super(SearchJobView, self).get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            context['save_job'] = Job.objects.filter(save_job__user_id=self.request.user.id).values_list('id', flat=True)
        return context


class UpdateJobView(SuccessMessageMixin,UpdateView):
    model = Job
    template_name = 'jobs/update.html'
    form_class = UpdateJobForm
    success_message = "You updated your job!"

    def form_valid(self, form):
        form.instance.employer = self.request.user
        return super(UpdateJobView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.employer != request.user:
            return HttpResponseRedirect('/')
        return super(UpdateJobView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('jobs:single_job',kwargs={"pk":self.object.pk,"slug":self.object.slug})


class DeleteJobView(SuccessMessageMixin,DeleteView):
    model = Job
    success_url = '/'
    template_name = 'jobs/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.employer == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.employer != request.user:
            return HttpResponseRedirect('/')

        return super(DeleteJobView, self).get(request, *args, **kwargs)


