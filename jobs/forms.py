import datetime
from django import forms

from jobs.models import Category, Job
from tinymce.widgets import TinyMCE


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = "__all__"


class JobForm(forms.ModelForm):
    description = forms.CharField(
        widget=TinyMCE())
    skills = forms.CharField(
        widget=TinyMCE())
    other_specification = forms.CharField(
        widget=TinyMCE())
    career_benefits = forms.CharField(
        widget=TinyMCE())

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields['category'].widget.attrs.update(
                {'class': 'custom-select'})

    class Meta:
        model = Job
        exclude = ["organization"]

    def validate_deadline(self, value):
        date_today = datetime.date.today()
        if value < date_today:
            raise forms.ValidationError("Please select valid deadline date.")
        return value
