from django.db import models
from users.abstract import DateTimeEntity
from users.models import UserProfile

class Resume(DateTimeEntity):
    profession = models.CharField(max_length=255, null=True, blank=True)
    summary = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name='resume')

    def __str__(self):
        return '%s - %s' % (self.profile.get_full_name(), self.summary)


class Experience(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    description = models.TextField(null=True, blank=True)
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name='experiences')

    def __str__(self):
        return self.title


class Skill(models.Model):
    title = models.CharField(max_length=255)
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name='skills')

    def __str__(self):
        return self.title


class Education(models.Model):
    university = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    description = models.TextField(null=True, blank=True)
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name='educations')

    def __str__(self):
        return self.university

