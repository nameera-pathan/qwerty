# Qwerty (job-portal-web)

Qwerty is a job portal web application.
It allows job seekers to create a profile, search and apply for job openings and receive selection and rejection messages if they got selected or rejected on any job.
It allows employers to post job openings, review and manage job applications and select or reject an employee on a job post they created.
It is a Django project that contains two apps called jobs and users.
A web application which is designed and implemented with Python and JavaScript.

## Features of Qwerty :

1. User registration : Users can create a new account by filling out a form and submitting it, A choice is given to the user to register as an employee or employer. The registration form includes fields such as email, firstname, lastname, birthday, location, password, password confirmation and finally a radio button to choose if user is employee or employer.
2. User login and logout : Both employee and employer can log in to their account using their email and password, and they can also log out of their account.
3. Pagination for displaying the Job Posts to easily navigate and browse through multiple job posts.
 
#### ` If user is Employee `

1. Homepage : At the homepage employee can search for jobs with the help of job filter which has three fields - "job title, job type, location" and can view job posts, number of jobs,profiles,resumes,companies in Qwerty.
3. Employee profile updates : Employees can update their profile information, such as - About, Education, skills, if they have socials or personal website/portfolio links and can upload their resume and can change their profile picture.
4. Save Jobs : This feature is only for employees, as employee can save their job if they wanna apply to it later or remove it from saved jobs.
5. Messages : This feature is also for employees only, employee can see the selection or rejection messages for the job post in which they got selected or rejected. If employee read selection/rejection message, the message background color will change to grey and If employe hasn't read selection/rejection message then the color of background will be white.
6. On a single job post : Employee can see the details of the job post and two buttons "Apply now" and "heart shaped save job button"
    ```
    a. Apply now - on click of "Apply now" button employee can apply for job post and after "Apply now" button clicked, 
       the button will get disabled and it's value will get changed to Applied.   
    b. heart shaped save job button - on click of save job button employees can save that job post and
       and remove that job post from saved jobs section.
    ```
    ```
    Note : If employee clicks on "Apply now" button, the single detailed job post will not show save job button.
    ```
7. Change Password : employee can use this feature to change password.
8. Employees can apply for jobs.
9. If employees forgets password, they can reset it: 

   ```
    For resetting password check -
   [Additional Information that staff should know] 
    section at the bottom of the readme file.
   ```

#### ` If user is Employer `

1. Homepage : It displays two buttons "Post a Job" and "My Posted Jobs", on click of "Post a job" employer can create a job post and on click of "My Posted Jobs" employer can view their posted jobs.
2. Job Post updates : Employers can update the job post information, such as - job title, Company name, location, job type, salary, skills required for job, qualification, if they have socials or personal website links and can update the company logo. 
3. On a single job post : Employer can see the details of the job post and three button "Applied Candidates" "Selected Candidates" "Rejected Candidates" and two buttons "delete" and "update"
    
    ```
    a. Applied Candidates - on click of Applied candidates button 
       employer can see the list of employees applied on that job post.
    b. Selected Candidates - on click of Selected candidates button employer can see the list of employees
       which employer selected from applied candidates section on that job post.
    c. Rejected Candidates - on click of Rejected candidates button employer can see the list of employees
       which employer rejected from applied candidates section on that job post.
    d. Delete - on click of Delete button employer can delete that job post.   
    e. Update - on click of Update button employer can update that job post.   
    ```
    
    ```
    Note : In Applied Candidates, Selected Candidates, Rejected Candidates sections employer sees the list of 
           employees and can view full employee profile by clicking on a button 
           (the button value will be employee name).
    ```
5. Change Password : employers can use this feature to change password.
6. If employers forgets password, they can reset it:
   ```
   For resetting password check -
   [Additional Information that staff should know] 
   section at the bottom of the readme file.
   ```

 
## How to run the application

##### To run the Qwerty app, follow these steps:

1. Navigate to the project folder/directory and create a virtual environment and activate it.
2. Run the following command to install the required Python packages listed in the requirements.txt file:
 
      ```
      pip install -r requirements.txt
      ```
3. Run the following commands in the terminal to create the database:
      
      ```
      python manage.py makemigrations
      python manage.py migrate
      ```
4. Run the application server with this command:      

      ```
      python manage.py runserver
      ```
5. Open your web browser and go to the URL `http://127.0.0.1:8000/` to access the home page of Qwerty.      

## Additional information

`Qwerty/settings.py -`

```
DEBUG = True

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
I used EMAIL_BACKEND for forgot password feature.
The DEBUG flag in Django is a boolean value that controls whether Django runs in debug mode or not.
Debug mode is used during development to provide more detailed error messages and other helpful debugging information.

When DEBUG is True, Django will use the console.EmailBackend email backend to send email messages to the console/terminal, rather than sending them over the network. It is used to see the email messages that are being sent, but they are not actually sent over the network.

##### Steps to reset the password -
1. At login page click on `forgot password ? [click here]` link.
2. Then enter you email address which you used to register on Qwerty.
3. After that a page will display this message 
   `We’ve emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly.
    If you don’t receive an email, please make sure you’ve entered the address you registered with.`
4. Then you'll see an email on console/terminal, just like this example given below.
   ```
   Content-Type: text/plain; charset="utf-8"
   MIME-Version: 1.0
   Content-Transfer-Encoding: 7bit
   Subject: Password reset on 127.0.0.1:8000
   From: webmaster@localhost
   To: xyz@example.com
   Date: Thu, 29 Dec 2022 20:54:49 -0000
   Message-ID: <167234728984.4760.1905825950277488021@1.0.0.127.in-addr.arpa>

   To reset the password for email xyz@example.com. Follow the link below:
   http://127.0.0.1:8000/users/reset/Mg/bh7ord-685854bd9422ddf3f0a662038fd88b46/
   ------------------------------------------------------------------------------
   ```
   copy whatever link it gives you from console/terminal, just like this link given in the example:
   `http://127.0.0.1:8000/users/reset/Mg/bh7ord-685854bd9422ddf3f0a662038fd88b46/`

5. Open your web browser, Paste the link in URL bar and press enter, it will navigate you to the password reset screen to reset your password.
6. Type your New Password and done.

_______________________________________

