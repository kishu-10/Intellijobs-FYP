# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from users.abstract import AddressEntity, DateTimeEntity


def dp_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'


class AuthUser(AbstractUser):
    """ Create New Auth User with added fields """

    USER_TYPE = [
        ('Organization', 'Organization'),
        ('Candidate', 'Candidate'),
        ('Staff', 'Staff')
    ]
    first_name = None
    last_name = None
    user_uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    is_email_verified = models.BooleanField(default=False)
    need_password_change = models.BooleanField(default=False)
    user_type = models.CharField(
        choices=USER_TYPE, default='Candidate', max_length=50)

    def __str__(self):
        return self.username


class UserProfile(AddressEntity):
    """ User Profile for Candidate """

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=500, unique=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    display_picture = models.ImageField(
        upload_to=dp_path, null=True, blank=True)
    dob = models.DateField(blank=True, null=True, verbose_name='Date of Birth')
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default='Male',
    )
    user = models.OneToOneField(
        to=AuthUser,
        on_delete=models.CASCADE,
        related_name='user_profile',
        null=True,
    )

    def __str__(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.get_full_name())
        return super().save(*args, **kwargs)


class OrganizationProfile(AddressEntity):
    """ Organization Profile for the organizations """

    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    display_picture = models.ImageField(
        upload_to=dp_path, null=True, blank=True)
    description = models.TextField()
    user = models.OneToOneField(
        to=AuthUser,
        on_delete=models.CASCADE,
        related_name='org_profile',
        null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


def cv_path(instance, filename):
    return f'user_{instance.candidate.user.id}/{filename}'


class CandidateCV(DateTimeEntity):
    """ CV for the candidates """

    cv = models.FileField(upload_to=dp_path)
    candidate = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='candidate_cv')


def doc_path(instance, filename):
    return f'user_{instance.organization.user.id}/{filename}'


class OrganizationDocuments(DateTimeEntity):
    """ Organization Documents for the organization """

    document = models.FileField(upload_to=doc_path)
    ogranization = models.ForeignKey(
        OrganizationProfile, on_delete=models.CASCADE, related_name='organization_paper')
