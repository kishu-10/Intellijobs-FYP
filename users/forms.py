from django import forms

from users.models import OrganizationProfile, UserProfile


class UserProfileForm(forms.ModelForm):
    """ Form to create and update User Profile """

    use_required_attribute = False

    class Meta:
        model = UserProfile
        exclude = ["user", "slug"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields['province'].widget.attrs.update(
                {'class': 'custom-select'})
            self.fields['district'].widget.attrs.update(
                {'class': 'custom-select'})


class OrganizationProfileForm(forms.ModelForm):
    """ Form to create and update Organization Profile """

    use_required_attribute = False

    class Meta:
        model = OrganizationProfile
        exclude = ["user", "slug",
                   "verification_status", "verification_status"]

    def __init__(self, *args, **kwargs):
        super(OrganizationProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields['province'].widget.attrs.update(
                {'class': 'custom-select'})
            self.fields['district'].widget.attrs.update(
                {'class': 'custom-select'})
