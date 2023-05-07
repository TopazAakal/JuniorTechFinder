from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator, FileExtensionValidator, MinValueValidator
from django.contrib.auth.models import User


class Recruiters(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, validators=[
        RegexValidator(r'^[a-zA-Z ]*$', 'Only letters and spaces are allowed.')
    ])
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, blank=True, validators=[
        RegexValidator(r'^\d{10}$', 'Only 10 digits are allowed.')
    ])
    city = models.CharField(max_length=100, validators=[
        RegexValidator(r'^[a-zA-Z0-9 ,.\'-]*$',
                       'Only letters, numbers, spaces, commas, periods, apostrophes and hyphens are allowed.')
    ])
    age = models.PositiveIntegerField(validators=[
        MinValueValidator(0, 'Age cannot be negative.')
    ])
    company = models.TextField()
    summary = models.TextField()
    photo = models.ImageField(upload_to='media', blank=True, null=True, validators=[
        FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'],
                               'Only jpg, jpeg, png and gif files are allowed.')
    ])


class JobListing(models.Model):
    FULL_TIME = 'FT'
    PART_TIME = 'PT'
    STUDENT = 'ST'
    INTERN = 'IN'
    JOB_TYPE_CHOICES = [
        (FULL_TIME, 'Full-time'),
        (PART_TIME, 'Part-time'),
        (STUDENT, 'Student'),
        (INTERN, 'Intern'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    recruiter = models.ForeignKey(Recruiters, on_delete=models.CASCADE)
    application_link = models.URLField(max_length=200)
    company_name = models.CharField(max_length=100)
    salary = models.PositiveIntegerField(blank=True, null=True)
    job_type = models.CharField(max_length=2, choices=JOB_TYPE_CHOICES)

    def __str__(self):
        return self.title
