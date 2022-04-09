# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from users.abstract import AddressEntity, DateTimeEntity
import os


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

    @property
    def has_dashboard_access(self):
        access = False
        if self.is_superuser:
            access = True
        elif self.user_type == "Staff":
            access = True
        elif self.user_type == "Organization" and self.org_profile.verification_status == "Verified":
            access = True
        return access

    @property
    def has_profile(self):
        if self.user_type == "Organization" and OrganizationProfile.objects.filter(user=self).exists():
            return True
        elif self.user_type == "Candidate" and UserProfile.objects.filter(user=self).exists():
            return True
        elif self.user_type == "Staff" or self.is_superuser:
            return True
        return False


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

    VERIFICATION_STATUS = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    display_picture = models.ImageField(
        upload_to=dp_path, null=True, blank=True)
    org_description = models.TextField(null=True, blank=False)
    verification_status = models.CharField(
        max_length=100, choices=VERIFICATION_STATUS, default="Pending")
    verified_by = models.ForeignKey(
        AuthUser, on_delete=models.SET_NULL, null=True, related_name="organization_verifier")
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


class CandidateCV(DateTimeEntity):
    """ CV for the candidates """

    cv = models.FileField(upload_to="candidate_cvs/")
    candidate = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='candidate_cv')

    def file_name(self):
        return os.path.basename(self.cv.name)


class OrganizationDocuments(DateTimeEntity):
    """ Organization Documents for the organization """

    document = models.FileField(upload_to="org_docs/")
    ogranization = models.ForeignKey(
        OrganizationProfile, on_delete=models.CASCADE, related_name='organization_paper')

    def file_name(self):
        return os.path.basename(self.document.name)
