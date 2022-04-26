from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class StaffRegistrationForm(forms.ModelForm):
    use_required_attribute = False
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def __init__(self, *args, **kwargs):
        super(StaffRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already exists.")
       return email
