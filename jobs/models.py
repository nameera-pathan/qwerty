from django.db import models
from django.template.defaultfilters import slugify
from PIL import Image
from Qwerty import settings
from taggit.managers import TaggableManager
# Create your models here.



class Job(models.Model):
    title = models.CharField(max_length=300)
    company = models.CharField(max_length=300)
    CHOICES = (
        ('full_time','Full Time'),
        ('part_time','Part Time'),
        ('freelance','Freelance'),
        ('internship','Internship'),
        ('temporary','Temporary'),
    )

    job_type = models.CharField(max_length=20,blank=False,default=None,choices=CHOICES)
    location = models.CharField(max_length=200,blank=False,default=None)
    companylogo = models.ImageField(upload_to="media/company",default="media/company/company.jpg")
    description = models.TextField(blank=False,default=None)
    salary = models.DecimalField(max_digits=12, decimal_places=2,default=0.00)
    publishing_date = models.DateTimeField(auto_now_add=True)
    qualification = models.CharField(max_length=200,blank=True,default='')
    skills = TaggableManager()
    website = models.URLField(blank=True,default='')
    twitter = models.URLField(blank=True,default='')
    instagram = models.URLField(blank=True,default='')
    facebook = models.URLField(blank=True,default='')
    slug = models.SlugField(default=None,editable=False)
    employer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=None)
    employee = models.ManyToManyField(settings.AUTH_USER_MODEL,default=None,blank=True,related_name="job_employee")

    def __str__(self):
        return self.title

    def save(self, *args,**kwargs):
        self.slug = slugify(self.title)
        super(Job, self).save(*args,**kwargs)
        img = Image.open(self.companylogo)
        if img.height > 200 or img.width > 200 :
            new_size = (200,200)
            img.thumbnail(new_size)
            img.save(self.companylogo.path)


class Meta:
    ordering = ('-id',)

