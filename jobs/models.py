from django.db import models

from users.abstract import DateTimeEntity

# Create your models here.

JOB_LEVEL_CHOICES = (
    ('Traineeship', 'Traineeship'),
    ('Internship', 'Internship'),
    ('Junior', 'Junior'),
    ('Mid', 'Mid'),
    ('Senior', 'Senior')
)

EMPLOYEMENT_TYPE_CHOICES = (
    ('Full', 'Full'),
    ('Part', 'Part'),
)


class JobAbstractModel(DateTimeEntity):
    title = models.CharField(max_length=150)
    no_of_vacancy = models.PositiveIntegerField()
    offered_salary = models.CharField(max_length=200)
    deadline = models.DateTimeField()
    education_level = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    skills = models.TextField()
    other_specification = models.TextField()
    career_benefits = models.TextField(null=True, blank=True)
    job_address = models.CharField(max_length=225, null=True, blank=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='categories_images/')

    def __str__(self):
        return self.name


class Job(JobAbstractModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='jobs')
    job_level = models.CharField(
        max_length=50, choices=JOB_LEVEL_CHOICES, default='Mid')
    employment_type = models.CharField(
        max_length=50, choices=EMPLOYEMENT_TYPE_CHOICES, default='Full')
    experienced_required = models.FloatField()

    def __str__(self):
        return self.title
