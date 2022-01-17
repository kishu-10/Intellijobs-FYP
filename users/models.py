# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from intellijobs.abstract import AddressEntity


class AuthUser(AbstractUser):
    ORGANIZATION = 'O'
    USER = 'U'
    ADMIN = 'A'
    USER_TYPE = [
        (ORGANIZATION, 'Organization'),
        (USER, 'User'),
        (ADMIN, 'Admin')
    ]
    user_uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=500, unique=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    need_password_change = models.BooleanField(default=False)
    user_type = models.CharField(choices=USER_TYPE, default=USER, max_length=1)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = self.slug
        else:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)


def dp_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'


class UserProfile(AddressEntity):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]

    user = models.OneToOneField(
        to=AuthUser,
        on_delete=models.CASCADE,
        related_name='user_profile',
        null=False,
    )
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    display_picture = models.ImageField(
        upload_to=dp_path, null=True, blank=True)
    dob = models.DateField(blank=True, null=True, verbose_name='Date of Birth')
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=FEMALE,
    )
    cv = models.FileField(upload_to="user/")

    def __str__(self):
        return ' '.join([
            self.user.first_name,
            self.user.last_name,
        ])


class OrganizationProfile(AddressEntity):
    user = models.OneToOneField(
        to=AuthUser,
        on_delete=models.CASCADE,
        related_name='org_profile',
        null=True
    )
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    description = models.TextField(blank=False, null=False)
    org_papers = models.ImageField(
        upload_to="organization/", blank=False, null=False)
