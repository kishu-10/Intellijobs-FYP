from django.db import models

from users.abstract import DateTimeEntity
from users.models import CandidateCV, OrganizationProfile, UserProfile

# Create your models here.

JOB_LEVEL_CHOICES = (
    ('Traineeship', 'Traineeship'),
    ('Internship', 'Internship'),
    ('Employee', 'Employee'),
)

EMPLOYEMENT_TYPE_CHOICES = (
    ('Full', 'Full'),
    ('Part', 'Part'),
)


class JobAbstractModel(DateTimeEntity):
    title = models.CharField(max_length=150)
    no_of_vacancy = models.PositiveIntegerField()
    offered_salary = models.CharField(max_length=200)
    deadline = models.DateField(null=True, blank=True)
    education_level = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    skills = models.TextField()
    other_specification = models.TextField(null=True, blank=True)
    career_benefits = models.TextField(null=True, blank=True)
    job_address = models.CharField(max_length=225, null=True, blank=True)
    is_active = models.BooleanField(default=1)
    organization = models.ForeignKey(
        OrganizationProfile, on_delete=models.CASCADE, related_name="jobs")

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
        max_length=50, choices=JOB_LEVEL_CHOICES, default='Employee')
    employment_type = models.CharField(
        max_length=50, choices=EMPLOYEMENT_TYPE_CHOICES, default='Full')
    experienced_required = models.FloatField()

    def __str__(self):
        return self.title


class JobApplication(DateTimeEntity):
    candidate = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='applied_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name='applications')
    cv = models.ForeignKey(
        CandidateCV, on_delete=models.CASCADE, related_name='applied_cv')

    def __str__(self):
        return self.candidate.get_full_name()


class JobWishlist(models.Model):
    owner = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return (str(self.owner) + ' wishlist')


class JobWishlistDetail(DateTimeEntity):
    wishlist = models.ForeignKey(
        JobWishlist, on_delete=models.SET_NULL, blank=True, null=True, related_name='wishlist_detail')
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, blank=True, null=True, related_name='wishlist_job')
    # is_active -> opposite of is_archive -> for deletion
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.job)
