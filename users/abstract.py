from django.db import models


class DateTimeEntity(models.Model):
    date_updated = models.DateTimeField(blank=True, auto_now=True)
    date_created = models.DateTimeField(blank=False, auto_now_add=True)

    class Meta:
        abstract = True


class Province(models.Model):
    name = models.CharField(max_length=255)
    province_code = models.CharField(max_length=255)


class District(models.Model):
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)


class Country(models.Model):
    name_iso_3166_a2 = models.CharField(max_length=10)
    printable_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)


class AddressEntity(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    province = models.ForeignKey(
        Province, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(
        District, on_delete=models.SET_NULL, null=True, blank=True)
    area = models.CharField(max_length=255, blank=False, null=True)
    city = models.CharField(max_length=255, blank=True, null=False)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.country
