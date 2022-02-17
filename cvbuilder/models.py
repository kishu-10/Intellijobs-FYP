from django.db import models
from users.abstract import DateTimeEntity
from users.models import UserProfile


CV_DATE_INPUT_FORMATS = ['%b %Y']


class Resume(DateTimeEntity):
    image = models.ImageField(upload_to='resume_images', null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    summary = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    github = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name='resume')

    def __str__(self):
        return '%s - %s' % (self.name, self.description)


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
    title = models.CharField(max_length=255)
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
        return self.title


class Achievement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name='achievements')

    def __str__(self):
        return self.title


class Language(models.Model):
    title = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name='languages')

    def __str__(self):
        return self.title
