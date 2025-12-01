
from django.urls import path, include
from .views import *
from django.contrib.auth import views as authViews


app_name = "users"
urlpatterns = [
    path('register/',UserRegisterView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('password-change/',authViews.PasswordChangeView.as_view(),name='password_change'),
    path('password-change-done/',authViews.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('update-profile/<int:pk>/',UserUpdateView.as_view(),name='update_profile'),
    path('employee-profile/<int:employee_id>/<int:job_id>/',EmployeeProfileView.as_view(),name='employee_profile'),
    path('my-profile/<int:pk>/',MyProfileView.as_view(),name='my_profile'),
    path('employer-jobs/',EmployerPostedJobsView.as_view(),name='employer_jobs'),
    path('employee-messages/<int:pk>/',EmployeeMessagesView.as_view(),name='employee_messages'),
    path('employee-display-messages/<int:pk>/',EmployeeDisplayMessages.as_view(),name='employee_display_messages'),
    path('save-job/<int:pk>/',SaveJobView.as_view(),name='save_this_job'),
    path('remove-from-savedjobs/<int:pk>/',RemoveFromSavedJobsView.as_view(),name='remove_from_savedjobs'),
    path('my-saved-jobs/<int:pk>/',MySavedJobsView.as_view(),name='my_saved_jobs'),
]
 